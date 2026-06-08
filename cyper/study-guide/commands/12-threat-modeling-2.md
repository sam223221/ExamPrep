# 12. Threat Modeling II — Commands & Code Examples

### List every pod across all namespaces (recon)
**What:** Inventory the running workloads cluster-wide — step 1 (Model the System) reconnaissance on K8s (L12 p.4, p.8).
```bash
# kubectl (standard syntax)
kubectl get pods -A
kubectl get pods --all-namespaces -o wide   # -o wide adds node + pod IP
```
**Notes:** `-A` / `--all-namespaces` is the recon staple — it reveals every workload, the node each runs on, and pod IPs. From a compromised container this maps the cluster's attack surface (the DFD components on p.8). `-o wide` exposes which node a pod sits on, useful for finding workloads scheduled on the master node (an etcd attack prerequisite, L12 p.10).

### Enumerate your own effective permissions (authz recon)
**What:** Ask the API server what the current identity is allowed to do — directly probes the "RBAC issues" attack vector (L12 p.9).
```bash
# kubectl (standard syntax)
kubectl auth can-i --list                       # all verbs/resources for me
kubectl auth can-i create deployments           # single check -> yes/no
kubectl auth can-i get secrets -n kube-system   # can I read secrets here?
```
**Notes:** `auth can-i --list` dumps every (verb, resource) the token may perform; `auth can-i <verb> <resource>` answers a single question. This is exactly the attacker check behind leaves like **[D13] service account has sufficient privilege** and **[SC1] RBAC permissions open on service token** (L12 pp.10, 14). As a defender, an over-broad `--list` output flags an RBAC mis-configuration.

### Check a service account's permissions by impersonation (authz audit)
**What:** Test whether a specific service account has more access than least-privilege requires (L12 pp.9, 15).
```bash
# kubectl (standard syntax) — --as / --as-group impersonation
kubectl auth can-i --list \
  --as=system:serviceaccount:default:my-app-sa
kubectl auth can-i get secrets \
  --as=system:serviceaccount:default:my-app-sa -n default
```
**Notes:** `--as=system:serviceaccount:<namespace>:<name>` impersonates the SA so you can audit its real reach without holding its token. If a workload SA can `get secrets`, the "Steal/exfiltrate secrets → RBAC allow secret retrieval" path (L12 p.14) is open — tighten the Role.

### Dump secrets and decode a value (recon / why ConfigMaps are wrong)
**What:** List secrets and read one — the action behind "Kubelet get all secrets for pods in namespace" (L12 p.14).
```bash
# kubectl (standard syntax)
kubectl get secrets -A
kubectl get secret my-app-secret -n default -o jsonpath='{.data.password}' | base64 -d
```
**Notes:** K8s Secret values are only base64-encoded (not encrypted by default), so `base64 -d` reveals them — this is why the lecture says store sensitive data in **K8s Secrets, not ConfigMaps**, and enable etcd encryption at rest (L12 pp.15, 326). If `get secrets -A` succeeds from a low-privilege token, RBAC is mis-configured. Decoding is read-only recon, not exploitation.

### List all Roles and RoleBindings cluster-wide (RBAC audit)
**What:** Map who can do what — find the over-permissive bindings that the lecture flags as the pervasive vector (L12 p.9).
```bash
# kubectl (standard syntax)
kubectl get roles,rolebindings -A
kubectl get clusterroles,clusterrolebindings
# inspect a suspicious binding
kubectl describe clusterrolebinding cluster-admin
```
**Notes:** Namespaced (`roles`/`rolebindings`) plus cluster-scoped (`clusterroles`/`clusterrolebindings`) together show the full authorization picture. Hunt for subjects bound to `cluster-admin` or `*` verbs/resources — those satisfy multiple attack-tree leaves at once. Fixing RBAC removes a prerequisite shared across paths (L12 p.296).

### Run a CIS benchmark conformance check with kube-bench (standard syntax)
**What:** Verify the cluster is *securely deployed* against the CIS Kubernetes Benchmark — the validation step (L12 pp.15, 17).
```bash
# kube-bench (Aqua) — standard syntax
kube-bench run                       # auto-detect node role
kube-bench run --targets master      # control-plane checks only
kube-bench run --targets node        # worker-node checks only
```
**Notes:** kube-bench is the lecture's tool for "is Kubernetes securely deployed?" (L12 p.168). Output is PASS/FAIL/WARN per CIS control with remediation text. `--targets` scopes checks to the component you can see (master vs node). Run it as part of step 4 (Validate) and after every config change to catch regressions.

### Scan a manifest for security risk with kubesec (standard syntax)
**What:** Static security-risk analysis of a single K8s resource file before it ships (L12 pp.17, 169).
```bash
# kubesec — standard syntax
kubesec scan deploy.yaml
# via the hosted API instead of the binary:
curl -sSX POST --data-binary @deploy.yaml https://v2.kubesec.io/scan
```
**Notes:** `kubesec scan <file>` returns a numeric score plus advice — it rewards `runAsNonRoot`, `readOnlyRootFilesystem`, dropped capabilities and penalizes privileged/hostPID/hostNetwork settings (the exact attack-tree leaf conditions on L12 pp.10, 12). A negative score means the manifest enables host-level attacks. Use it in CI to block risky deployments.

### Scan cluster, manifests, and images with kubescape (standard syntax)
**What:** Broad security scan across cluster, manifest files, repos and images against frameworks like NSA/CIS (L12 pp.17, 171).
```bash
# kubescape — standard syntax
kubescape scan                                  # whole live cluster
kubescape scan framework nsa                     # against the NSA framework
kubescape scan deploy.yaml                        # a single manifest
kubescape scan image myregistry/app:1.4.2         # an image
```
**Notes:** Kubescape is the lecture's "scans clusters, manifest files, code repos, container registries and images" tool (L12 p.171) — the broadest of the named scanners. Bare `scan` audits the connected cluster; pass a framework, file, or image to narrow it. It surfaces RBAC, network-policy, and privileged-container findings that map straight back to the attack vectors on p.9.

### Statically scan a container image for vulnerabilities with Clair / Trivy (standard syntax)
**What:** Find known CVEs in an image before it runs — "static analysis of vulnerabilities in containers" (L12 pp.16, 17, 170).
```bash
# Trivy (standard syntax) — image vulnerability scan
trivy image myregistry/app:1.4.2
trivy image --severity HIGH,CRITICAL myregistry/app:1.4.2

# Clair (standard syntax) — via the clairctl client against a Clair server
clairctl report myregistry/app:1.4.2
```
**Notes:** Clair is the lecture's named image scanner; Trivy is the common drop-in that performs the same static CVE analysis. This implements the best practice "check for vulnerabilities periodically" and "know your base image" (L12 p.16). `--severity HIGH,CRITICAL` filters noise. Scan by digest, not `:latest`, so you know exactly what was assessed.

### Sign and verify an image with Notary / cosign (standard syntax)
**What:** Sign artifacts and verify signatures so a *poisoned* image is rejected — the pull-secret/registry-poisoning mitigation (L12 pp.12, 17, 172).
```bash
# Notary (Notary Project) — standard syntax: sign then verify
notation sign myregistry/app:1.4.2
notation verify myregistry/app:1.4.2

# cosign (standard syntax) — equivalent sign/verify
cosign sign myregistry/app@sha256:<digest>
cosign verify --key cosign.pub myregistry/app@sha256:<digest>
```
**Notes:** Notary "signs and verifies artifacts" and secures update distribution (used in Docker Trusted Registry) (L12 p.172); cosign is the common Sigstore equivalent. Verification breaks attack tree 3 — even if an attacker poisons the registry, an unsigned/altered image fails `verify` and is not admitted. Sign by digest (`@sha256:...`), never by mutable tag.

### Apply a restrictive default-deny NetworkPolicy (hardening config)
**What:** Close the "pods talk to each other by default" gap — counters the Network Endpoints attack vector (L12 pp.9, 15).
```yaml
# NetworkPolicy — default-deny ALL ingress + egress in a namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}            # empty selector = every pod in the namespace
  policyTypes:
    - Ingress
    - Egress
```
**Notes:** "All pods can talk to each other by default; you must add a network policy" (L12 p.149). An empty `podSelector: {}` with both policy types and no `ingress`/`egress` rules denies all traffic — the secure baseline. Layer narrow allow-policies on top of this. Without a CNI that enforces NetworkPolicy, the object is silently ignored — verify your CNI supports it.

### Allow only specific traffic on top of default-deny (hardening config)
**What:** Permit one frontend to reach the API pods on a single port and nothing else (least-privilege networking) (L12 pp.9, 15).
```yaml
# NetworkPolicy — allow frontend -> api on TCP 8080 only
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
```
**Notes:** Policies are additive and whitelist-only — this grants `frontend` -> `api:8080` while the default-deny policy blocks everything else. Restricting reachable endpoints shrinks the "access to endpoints if the pod's network policy permits" vector (L12 p.89). Match by label, not pod name, so the rule survives pod restarts.

### Define a least-privilege RBAC Role + RoleBinding (hardening config)
**What:** Grant a service account exactly the verbs/resources it needs — directly counters the RBAC-issues vector (L12 pp.9, 15).
```yaml
# Role: read-only on pods + their logs, in one namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]   # no create/delete, no secrets
---
# RoleBinding: attach the Role to one service account
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: my-app-sa
    namespace: production
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```
**Notes:** A namespaced `Role` (not `ClusterRole`) plus `RoleBinding` scopes power to one namespace. Note there is **no** `secrets` resource and **no** `create`/`delete` — this defeats the "RBAC allow secret retrieval" and scale-deployment leaves (L12 pp.10, 14). Least privilege is the antidote to "many attack vectors rely on RBAC mis-configuration" (L12 p.9). Verify with `kubectl auth can-i --list --as=system:serviceaccount:production:my-app-sa`.

### Lock down a Pod with a hardened SecurityContext (hardening config)
**What:** Run non-root, read-only root FS, no privilege escalation, all Linux capabilities dropped — kills multiple recurring attack-tree leaves (L12 pp.10, 12, 16).
```yaml
# Pod/Deployment spec excerpt — pod- and container-level SecurityContext
apiVersion: v1
kind: Pod
metadata:
  name: hardened-app
spec:
  securityContext:                 # pod-level
    runAsNonRoot: true
    runAsUser: 10001
    fsGroup: 10001
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: myregistry/app@sha256:<digest>   # pin by digest, not :latest
      securityContext:             # container-level (overrides pod-level)
        allowPrivilegeEscalation: false
        privileged: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
```
**Notes:** Each setting closes a leaf: `runAsNonRoot`/`runAsUser` -> "don't run as root" (L12 p.161); `privileged: false` -> blocks "use a privileged container to start a process on the host" (L12 pp.10, 12); `readOnlyRootFilesystem` -> blocks "modify file on host filesystem [M7]"; `drop: ["ALL"]` -> removes SYS_PTRACE and friends ([M9], L12 p.126); pinning by digest -> "don't rely on :latest" (L12 p.159). This single block hardens many attack-tree paths at once.

### Enforce the restricted profile with Pod Security Admission (hardening config / PSP-style note)
**What:** Cluster-level guardrail that rejects privileged/hostPID/host-mount pods at admission — successor to deprecated PodSecurityPolicy (L12 p.150).
```yaml
# Namespace labels enabling Pod Security Admission (built-in, PSA)
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted   # reject violating pods
    pod-security.kubernetes.io/audit: restricted      # log violations
    pod-security.kubernetes.io/warn: restricted        # warn on apply
```
**Notes:** The lecture lists "Pod Security Policies — add pod security policies" (L12 p.150). PSP is removed in modern K8s; the standard replacement is **Pod Security Admission** via these namespace labels. The `restricted` level forbids privileged containers, `hostPID`/`hostNetwork`, host-path mounts and requires `runAsNonRoot` — enforcing in one place what the per-pod SecurityContext sets per workload. `enforce` blocks; `audit`/`warn` give a safe rollout path.

### Limit host mounts and forbid the docker socket (hardening rationale)
**What:** Prevent the recurring "mounted docker socket / host filesystem access" leaves that grant container escape (L12 pp.10, 12, 16).
```yaml
# AVOID this — a hostPath mount of the docker socket = container escape
# volumes:
#   - name: docker-sock
#     hostPath:
#       path: /var/run/docker.sock     # DANGEROUS

# Prefer: NO hostPath volumes, ephemeral storage only
spec:
  containers:
    - name: app
      volumeMounts:
        - name: scratch
          mountPath: /tmp
  volumes:
    - name: scratch
      emptyDir: {}                       # ephemeral, no host access
```
**Notes:** "Limit host mounts" is an explicit best practice (L12 p.162). A mounted `/var/run/docker.sock` lets a compromised container drive the host runtime — that is leaf **[M8] start process using container runtime** (L12 p.126). Using `emptyDir` instead of `hostPath` removes "find Pod/Container with access to host filesystem" ([M7]) and "with mounted docker socket". Block these at admission with the `restricted` PSA profile above.

### Sketch an AND/OR attack tree for the K8s DoS goal (attack-tree template)
**What:** Decompose the "DoS the cluster" root into OR alternatives and AND prerequisites — the core technique of the lecture (L12 pp.10–11).
```text
GOAL (root): DoS the Kubernetes cluster                    [OR]
|
+-- OR  Exhaust compute resources
|     +-- OR  Create a scale deployment via the API server     [AND]
|     |     +-- [D13] Service account has sufficient privilege
|     |     +-- [D14] Find a valid service-account token
|     +-- OR  Bring the Kubelet down  -> DoS Kubelet port 10250 [D11] / 10255 [D10] / 10248 [D12]
|
+-- OR  Disrupt control plane (rate/restart scheduling)
|     +-- OR  Loss of etcd quorum   -> DoS etcd 2379 [D5] (client) / 2380 [D5] (peer)
|     +-- OR  Bring scheduler down  -> DoS scheduler 10251 [D4] / 10259 [D3]
|     +-- OR  Bring controller-mgr  -> DoS controller 10252 [D6] / 10257 [D7]
|     +-- OR  DoS API server         -> port 6443 [D1] / 8080 [D2]
|
+-- OR  Disrupt networking
      +-- OR  Bring kube-proxy down -> port 10249 [D8] / 10256 [D9]
      +-- OR  DoS K8s DNS            -> port 53 (queries fail)
      +-- OR  Saturate / degrade the CNI overlay network
```
**Notes:** Read top-down, root -> leaf. **OR** = any one child suffices (block *every* alternative). **AND** = all children required (block *any one* link to break the chain) — so the cheapest defence on the scale-deployment branch is to deny either [D13] or [D14] via least-privilege RBAC. The `[D#]` labels and ports are the MCQ-baitable detail (L12 p.120); the takeaway is "each component listens on a port, so each port is a DoS target" (L12 p.290).

### Review audit logs to validate mitigations (detection)
**What:** Periodically watch the API-server audit log — the lecture's Audit Logging security feature, used for detection/validation (L12 p.148).
```bash
# kubectl (standard syntax) — read recent API activity for live triage
kubectl get events -A --sort-by=.lastTimestamp

# Inspect the API server audit log on the control-plane node (path is config-dependent)
tail -f /var/log/kubernetes/audit/audit.log
```
**Notes:** "Audit Logging — periodically watch audit logs" (L12 p.148) is step 4 (Validate) in action — it detects exploitation of the modeled threats (suspicious `create`/`exec`/`get secrets` calls). `kubectl get events` is the quick triage view; the audit log (enabled via an audit policy on the API server) is the authoritative record. Detection complements prevention: RBAC/NetworkPolicy stop the attack, audit logs prove they worked.
