# Case Study 1: The Linux Network Stack (Hrvoje Horvat, v1.45)

> **Source:** case-1.pdf — 1 page, a single very large A2-sized landscape poster diagram. PyMuPDF counts ~945 vector primitives composing the figure; the artifact is essentially a high-density architectural map of an entire real-world system.
> **Likely tied to:** **Lecture 1** (introduces "Case #1" by Hrvoje Horvat 2024 explicitly), and used as a *running concrete example* across **Lectures 2–4** (quality attributes, tactics, patterns) and parts of **Lecture 5–7** (deployment / virtualization / distribution). It is the course's flagship "look at one real system and identify everything we have been talking about" artifact.

![Full Linux network stack poster (Horvat v1.45)](../images/case_1/case1_full_diagram.png)

## Scenario

The case study is a **single architectural poster** that maps the **complete data path of a network packet** through a modern Linux host that is *also* acting as a hypervisor for KVM virtual machines and as an OpenStack compute / network node. There is no "narrative" prose; the case study **is** the diagram. The student is expected to be able to:

1. Trace a packet end-to-end (application → socket → TCP/UDP → IP → qdisc → driver → NIC, and the symmetric receive path back up).
2. Identify, at every layer, **which architectural elements are involved**, **which configuration knobs (sysctls / ethtool flags) tune them**, and **which Linux command observes them**.
3. Relate the boxes on the poster back to the **architectural concepts** from the course: layering, separation of concerns, virtualization, namespacing, intermediaries (bridges/switches), buffering, scheduling, offloading, and the quality-attribute trade-offs each of those choices makes.

The implicit "problem" the case explores is the canonical one of the course: **how does a single large, performance-critical, multi-tenant operating-system component stay modifiable, performant, available, secure and operable simultaneously** — and what concrete tactics and patterns are visible inside it. Linux's network stack is a great teaching case because every architectural style and tactic the course covers (layering, pipe-and-filter, broker/bridge, virtualization, replication-of-state via VETH pairs, namespacing-as-isolation, hardware-offload-as-performance-tactic, etc.) is physically present.

The diagram covers four "worlds" stacked together:

- **Host Linux user-space + kernel stack** (right half): applications → socket layer → TCP/UDP → IP → traffic-control / qdisc → device driver → NIC hardware, with Netfilter, NAPI, GRO/GSO/RPS/RFS, XDP and eBPF labelled.
- **Virtualization slice** (top-left): a guest VM running on **KVM + QEMU**, with either a fully emulated NIC (Intel 82540EM) or the **paravirtual virtio_net** front-end / back-end pair.
- **Container slice** (left middle): an **LXC container** with its own **namespaces** (mount, PID, UTS, user, network, cgroup) connected outward via a **VETH pair**.
- **Software-defined networking slice** (bottom): **Linux bridge** and **Open vSwitch (OVS)** with `br-int` / `br-tun`, **VLAN** and **VxLAN** ports, the OpenStack `qbr/qvb/qvo` naming convention, and **patch ports** between bridges.

## Stakeholders & context

The diagram is "owned" by everyone who must reason about traffic through a Linux box, but in the course's framing the stakeholders are:

- **Application developers** — care that sockets behave correctly, latency is bounded, and the kernel respects buffer sizes.
- **System administrators / SREs** — own the sysctl variables (`net.core.*`, `net.ipv4.*`), qdiscs, `ethtool -K` offload flags, IRQ affinity, and observability via `netstat`, `ss`, `sar`, `/proc/net/*`.
- **Kernel network maintainers** — must keep the layered design modifiable so new transport protocols (QUIC, MPTCP), new offloads (BIG TCP in 6.3+), and new SDN data planes (XDP, eBPF) can be added without breaking everything.
- **Cloud/virtualization operators (OpenStack, Proxmox)** — wire together VMs, containers, OVS bridges, VLAN/VxLAN tunnels, and need predictable performance under multi-tenant isolation.
- **Security engineers** — depend on Netfilter (`iptables`, `nftables`, `ebtables`, `arptables`, `conntrack`) sitting *between* the bridge and the IP layer, and on namespace isolation as a tenant boundary.

Constraints driving the design:

- Hard real-world performance ceiling: 1–100 Gbps line rates with limited CPU per core, which forces **batching (NAPI), offload to hardware (TSO, LRO, RSS, aRFS, checksum), and lock-free per-CPU queues (RPS/XPS)**.
- Backwards compatibility: 30+ years of socket API and sysctl names cannot break.
- Multi-tenancy: VMs and containers must share one NIC without seeing each other's traffic — requires bridging, VLAN/VxLAN, namespaces, and Netfilter hooks at multiple points.

## Quality attributes in play

The poster is essentially a checklist of QAs from Lectures 2–4 rendered as a real system:

- **Performance** — dominant QA. Concrete scenarios:
  - "Stimulus: 10 Gbps of small packets arriving on `eth0`. Response: kernel processes them without dropping. Measure: `/proc/net/softnet_stat` shows no drops." → Tactics on display: **NAPI polling** (`net.core.netdev_budget`, `..._usecs`, `dev_weight`), **RSS** multi-queue, **RPS/RFS/aRFS** for CPU steering, **GRO/LRO** for aggregation, **TSO/GSO** on transmit, **BIG TCP** (≥ kernel 6.3), **checksum offload**, **scatter-gather**, **XDP** for fastest-possible drop/redirect.
- **Modifiability** — every layer is replaceable: any TCP **congestion-control algorithm** (`net.ipv4.tcp_congestion_control`), any **qdisc** scheduler (`net.core.default_qdisc`, `tc qdisc add ...`), any **device driver** behind a stable NAPI contract, any **bridge implementation** (Linux bridge vs OVS) with identical wiring semantics. eBPF/XDP lets new behaviour be loaded without recompiling the kernel.
- **Availability** — bonding/teaming (LACP via `ifenslave`) gives multi-NIC failover; VRRP support via `net.ipv4.ip_nonlocal_bind`; conntrack survives across rules updates.
- **Security** — Netfilter is positioned **as a cross-cutting filter** that all interfaces pass through (ebtables/arptables at L2, iptables/nftables at L3, conntrack for stateful). Namespaces (network + user + PID) act as **isolation tactics**; VLAN and VxLAN provide **separation between tenants** on shared physical links.
- **Operability / observability** — every box on the diagram has a matching `/proc/net/*` file, `netstat`/`ss`/`sar`/`ethtool -S`/`ip -s link` command. The architect deliberately exposed counters at each layer.
- **Interoperability** — VirtIO (paravirtual) coexists with full hardware emulation; OVS speaks both VLAN and VxLAN; Linux bridge and OVS bridge are interchangeable plug-ins.

## Architectural decisions / patterns used

### 1. Strict layering as the spine of the host stack
- **Decision:** Applications → System Call Interface → Socket layer → TCP/UDP/IP → Netfilter → qdisc → Device driver → Ring buffers → NIC hardware. Each layer talks only to the one above and below.
- **Rationale:** This is the textbook **Layered architectural pattern** from Lecture 7. Every layer is independently testable, observable, and replaceable (e.g., swap TCP CUBIC for BBR via one sysctl).
- **Trade-off:** Performance cost of crossing layers — paid back via **batching (NAPI, GRO/GSO)** and **offload tactics** that let layers "skip ahead" when hardware can do the work. Classic modifiability-vs-performance trade-off from L2.
- **Diagram:**

![Host stack: applications → socket → TCP/UDP → IP → qdisc → driver, plus key sysctl tunables](../images/case_1/case1_host_stack_socket_tcp_ip.png)

### 2. Pipe-and-filter with hooks (Netfilter)
- **Decision:** Insert a **Netfilter** filtering interposer at *every* point where packets cross interfaces (bridge, IP, ingress, egress). Hook points: PREROUTING, INPUT, FORWARD, OUTPUT, POSTROUTING.
- **Rationale:** Cross-cutting **security tactic** ("Limit access", "Detect intrusion") realised as a **broker / interceptor**, see L4 tactics for security. A single mechanism enforces firewalling for *all* interfaces — physical, bridge, VETH, VLAN, VxLAN.
- **Trade-off:** Adds per-packet latency. Mitigation: rules compiled to bytecode (nftables / eBPF), conntrack hashtables, and the fact that XDP can bypass Netfilter for the very-hot path.

### 3. Virtualization via VirtIO paravirtual driver (front-end / back-end split)
- **Decision:** Guest VM gets a paravirtual NIC (`virtio_net`) instead of a fully emulated Intel 82540EM. The guest driver (front-end) talks to a host back-end through shared ring buffers, mediated by **KVM** + **QEMU**.
- **Rationale:** Performance tactic for the virtualization layer — full emulation forces QEMU to trap every register write; paravirt batches operations across the boundary. Also a **Bridge / Adapter pattern**: the same Linux socket stack on either side, just with a different "wire."
- **Trade-off:** Guest OS must know it is virtualized (loses some transparency of full emulation). Mitigation: both modes coexist in the diagram — you choose the trade-off per VM.
- **Diagram:**

![VM, VirtIO front-end / back-end, KVM hypervisor, full-emulation alternative](../images/case_1/case1_vm_virtio_kvm.png)

### 4. Namespaces as the isolation tactic for containers
- **Decision:** An LXC container has six namespaces (mount, PID, UTS, user, network, cgroup) plus cgroups for resource limits (RAM/CPU/disk/net). It connects to the outside world only through a **VETH pair** that bridges into the host's Linux bridge / OVS.
- **Rationale:** Cheapest possible "VM-like" isolation — no hypervisor, just relabelled kernel objects. Realises the **Sandbox / Resource manager** tactics from L4 (security & resource management).
- **Trade-off:** Weaker isolation than a real VM (shared kernel ⇒ kernel exploits cross the boundary). Mitigation: user namespaces map root-in-container to non-root-on-host; seccomp filters lock down syscalls.

### 5. Software-defined bridging: Linux bridge vs Open vSwitch
- **Decision:** Two interchangeable bridge implementations are shown side-by-side. **Linux bridge** is simple L2; **OVS** adds OpenFlow, VLAN tagging on every port, **VxLAN tunneling**, and the OpenStack-canonical `br-int` ↔ `br-tun` topology with **patch ports**.
- **Rationale:** **Pluggability** tactic for modifiability — operators can start with Linux bridge and migrate to OVS without changing how VMs attach (still a TAP into a bridge). VxLAN solves the L2-over-L3 problem for multi-host clouds.
- **Trade-off:** OVS adds operational complexity (flow tables, user-space `ovs-vswitchd`) for the gain of programmable forwarding.
- **Diagram:**

![Linux bridge vs Open vSwitch with br-int/br-tun, patch ports, VLAN and VxLAN](../images/case_1/case1_ovs_bridge_namespaces.png)

### 6. Hardware acceleration as a performance tactic at the boundary
- **Decision:** Push as much work into the NIC silicon as the NIC supports — RSS, aRFS, LRO, TSO, GSO, checksum offload, scatter-gather, VLAN tag insertion/strip, multi-queue (`ethtool -L`), even XDP at the driver entry point.
- **Rationale:** The "specialize a critical resource" performance tactic. Each `ethtool -K` toggle is an explicit knob exposing a trade-off.
- **Trade-off:** Offloads can mask bugs (a NIC computing checksums wrong is hard to detect) and may interact badly with virtualization (offloaded frames look strange to other VMs' stacks). The diagram exposes all the toggles so an operator can disable them when debugging.
- **Diagram:**

![NIC hardware offload (RSS, aRFS, LRO, TSO, checksum), IRQ affinity, ring buffers, XDP entry](../images/case_1/case1_nic_hw_offload.png)

### 7. Buffering at every queueing point
- **Decision:** Explicit buffers everywhere: socket buffers (`SKB`, `tcp_rmem/wmem`, `udp_*`), backlog buffer (`netdev_max_backlog`), TX qdisc + qdisc memory limit, `txqueuelen` (FIFO), driver ring buffers (HW FIFO via `ethtool -G`), options buffer (`optmem_max`).
- **Rationale:** Each buffer is an explicit **performance / availability tactic** — absorb bursts, decouple producer from consumer. The poster *names every buffer and its tuning knob*, which is itself an architectural choice: make the design **operable and observable**.
- **Trade-off:** Bufferbloat — too-deep buffers add latency. Mitigation: modern qdiscs like `fq_codel` / `fq` actively manage queue depth; the poster points at `net.core.default_qdisc` as the lever.

### 8. NAPI: hybrid interrupt + polling
- **Decision:** Driver raises one interrupt to enter NAPI mode, then **polls** the ring buffer until empty (bounded by `netdev_budget` / `netdev_budget_usecs` / `dev_weight`).
- **Rationale:** Performance tactic to amortize IRQ cost under load. Switches dynamically between latency-optimal (interrupt) and throughput-optimal (poll) regimes.
- **Trade-off:** Tail latency under low load is slightly higher than pure interrupts.

## Lessons learned / key takeaways

- **A real OS subsystem is a layered architecture in textbook form.** The poster is essentially Bass–Clements–Kazman Chapter on "Layered" with a real implementation underneath. Use it as your mental anchor whenever the exam asks you to *recognise* a layered pattern.
- **Every quality attribute leaves a fingerprint as a tunable.** Every sysctl, every `ethtool -K` flag, every `/proc/net/*` file is the **operability tactic** "expose configuration / measurement at architectural boundaries" made real.
- **Performance is bought with batching, offloading and per-CPU partitioning, not magic.** NAPI, GRO/GSO/TSO, RSS/RPS/RFS/aRFS, XDP — these are the recurring patterns. Be able to name two or three at speed.
- **Isolation has a price ladder:** namespaces (cheapest) → VirtIO paravirt VM → fully emulated VM (most expensive, most compatible). Pick the cheapest level that satisfies the threat model.
- **Pluggability everywhere:** congestion-control, qdisc, bridge implementation, NIC driver, hypervisor backend — each is an interface with multiple implementations behind it. That is the **modifiability** tactic "abstract common services / hide information."
- **The same `Netfilter` cross-cuts every interface type.** Cross-cutting concerns belong in interceptors, not duplicated per component — a recurring exam answer.
- **Buffers everywhere come with the bufferbloat trade-off** — a perfect illustration of "performance and latency can pull in opposite directions" from L2.
- **Observability was designed in, not bolted on:** counters at every layer (`/proc/net/dev`, `softnet_stat`, `ss`, `netstat`, `sar`, `ethtool -S`). The poster *is* the documentation, which itself is an operability tactic.

## Exam relevance

This case is almost designed to be asked in the form: **"Look at this diagram (or this part of it) and identify three architectural patterns, three tactics, and one trade-off."** Concretely, expect to:

- **Name patterns** present and justify: Layered (host stack), Pipe-and-filter / Broker (Netfilter, qdisc), Bridge/Adapter (VirtIO, Linux bridge vs OVS), Sandbox (namespaces), Master/Worker-style multi-queue (RSS), Shared-data (ring buffers, SKBs).
- **Map QAs to mechanisms.** Given "performance," cite NAPI + offloads. Given "modifiability," cite the pluggable congestion-control / qdisc / bridge. Given "security," cite Netfilter + namespaces + VLAN/VxLAN isolation. Given "availability," cite bonding/LACP.
- **Articulate trade-offs.** Performance vs latency (bufferbloat), isolation strength vs cost (namespace vs VM), offload speed vs debuggability, layering modularity vs cross-layer overhead.
- **Trace a packet.** Given a scenario like "a VM in OpenStack sends a TCP packet to another VM on a different compute node," walk the path: guest app → guest socket/TCP/IP → virtio_net front-end → virtio_net back-end (host) → TAP → qbr Linux bridge → qvb/qvo VETH pair → OVS `br-int` (adds VLAN tag) → patch port → OVS `br-tun` (VxLAN encapsulates) → eth0 qdisc → driver → NIC. This kind of trace is extremely likely.
- **Recognize the diagram itself.** If a cropped region appears, identify which subsystem (VirtIO? OVS? hardware offload? namespaces?) and which lecture concepts it illustrates.

## Cross-references to lectures

- **Lecture 1** — explicitly introduces "Case #1" pointing to Hrvoje Horvat (2024); this is that diagram. Use it as the running example any time the course speaks of "a real system."
- **Lecture 2 (Quality attributes / scenarios)** — every QA scenario (performance, modifiability, availability, security, operability) is instantiated here with concrete stimulus / measure pairs.
- **Lecture 3 (Architecture in context / design process)** — illustrates how operators are themselves stakeholders, and how observability and configuration are first-class architectural requirements.
- **Lecture 4 (Tactics)** — almost every tactic class is visible:
  - *Performance:* introduce concurrency (multi-queue, RPS), bound queue size (`txqueuelen`, qdisc memory), reduce overhead (offloads), schedule resources (qdisc algorithms, IRQ affinity).
  - *Modifiability:* abstract common services (NAPI contract, qdisc API), hide information (driver behind kernel API), use intermediaries (Netfilter, bridges).
  - *Availability:* redundancy (bonding/LACP), failover (VRRP via `ip_nonlocal_bind`), state monitoring (`/proc/net/*`).
  - *Security:* limit access (Netfilter), separate entities (namespaces, VLAN/VxLAN), validate inputs (conntrack).
- **Lecture 5 / 6 (Patterns and styles)** — clear instances of Layered, Pipe-and-filter, Broker/Bridge, Sandbox, and Shared-data patterns side-by-side.
- **Lecture 7 (Distribution / deployment)** — OVS with VxLAN tunnels between compute and network nodes is the OpenStack reference deployment topology.
- **Lecture 8 (Virtualization / containers)** — KVM+QEMU+VirtIO and the LXC namespace bundle are the canonical hypervisor and container examples used by the course.
- **Likely callback in later lectures** — any lecture that talks about microservices networking, service meshes, or eBPF observability will lean on this poster again because eBPF/XDP are the hot edge of the same diagram.
