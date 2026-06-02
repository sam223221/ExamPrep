# Feature Plan: xCalculator

> Companion to the spec: `docs/superpowers/specs/2026-06-02-xcalculator-design.md`.
> The spec is the source of truth for behavior; this plan covers orchestration,
> file ownership, and acceptance gates.

## 1. Scope

Build `AI/xCalculator/` — a React + Vite + TypeScript desktop app (Electron, packaged as a
portable Windows `.exe`) with four tabs:

1. **Calculator** — arithmetic via a safe shunting-yard parser.
2. **Probability** — combinatorics (`n!`, `nPr`, `nCr`), probability rules, Bayes' theorem.
3. **Bayesian Network** — React Flow canvas (add nodes, drag arrows, edit CPTs), exact
   inference by enumeration `P(query | evidence)`.
4. **HMM** — Forward (P(O) + α trellis) and Viterbi (best path + δ/backpointer tables).

**Acceptance criteria:** see spec §1. Headline checks: BN reproduces AIMA Alarm
`P(Burglary|JohnCalls,MaryCalls) ≈ 0.284`; HMM reproduces Lab 8 ice-cream Forward/Viterbi;
`npm run dist` yields `release/xCalculator.exe`.

**Out of scope:** spec §1 (no BN learning, no HMM Backward/Baum-Welch, no continuous
distributions, no networking).

## 2. Files to Add

Full tree in spec §2. Grouped by owner below (§4).

## 3. Files to Modify

None — greenfield subfolder.

## 4. Agent Assignments & File Ownership (disjoint — no two agents share a file)

**Phase 1 — pm-setup (scaffold, runs alone first):**
- `package.json`, `tsconfig*.json`, `vite.config.ts`, Electron+Vite integration config,
  `electron-builder` config, `index.html`, `.gitignore`, `README.md`
- `electron/main.ts`, `electron/preload.ts`
- `src/main.tsx`, `src/index.css`, `src/App.tsx`, `src/components/Tabs.tsx`
- **Placeholder** components (real exports, "coming soon" body) so App compiles:
  `src/components/calculator/Calculator.tsx`, `src/components/probability/Probability.tsx`,
  `src/components/bayes/BayesNetwork.tsx`, `src/components/hmm/Hmm.tsx`
- Installs **all** dependencies (incl. `@xyflow/react`) so feature agents never touch
  `package.json`.
- Exit gate: `npm install` clean; app builds; dev launch config works.

**Phase 2a — pm-frontend (Calculator + Probability):** owns and fills
- `src/lib/calc.ts`, `src/components/calculator/Calculator.tsx`
- `src/lib/probability.ts`, `src/components/probability/Probability.tsx`
- `src/lib/__tests__/calc.test.ts`, `src/lib/__tests__/probability.test.ts`

**Phase 2b — pm-frontend (Bayes + HMM):** owns and fills
- `src/lib/bayes/types.ts`, `src/lib/bayes/inference.ts`,
  `src/components/bayes/{BayesNetwork,BayesNode,CptTable,QueryPanel}.tsx`
- `src/lib/hmm/types.ts`, `src/lib/hmm/forward.ts`, `src/lib/hmm/viterbi.ts`,
  `src/components/hmm/{Hmm,MatrixEditor,TrellisTable}.tsx`
- `src/lib/__tests__/bayes.test.ts`, `src/lib/__tests__/hmm.test.ts`

Phase 2a and 2b are independent (disjoint files; do not touch `App.tsx`, `Tabs.tsx`, configs,
or `package.json`) and run in parallel.

**Phase 3 — pm-qa:** read-only verification + may run build/test commands.
**Phase 4 — pm-reviewer:** read-only PR-style review.

## 5. Dependencies & Order

1. Phase 1 (pm-setup) — must finish first; everything depends on the skeleton + installed deps.
2. Phase 2a + 2b — parallel, after Phase 1.
3. Phase 3 (pm-qa) — after 2a & 2b.
4. Phase 4 (pm-reviewer) — after QA; loop fixes via pm-frontend on P0/P1.

## 6. Security Considerations

- **No `eval`** anywhere — calculator uses a hand-written shunting-yard parser.
- Electron hardening: `contextIsolation: true`, `nodeIntegration: false`, a minimal/empty
  `preload`. App loads only local bundled files (`file://`); no remote content, no `webSecurity`
  disabling.
- All numeric inputs validated/clamped (probabilities to `[0,1]`, `nCr`/`nPr` guards). No
  network calls, no filesystem writes beyond user-initiated JSON export and `localStorage`.
- Import of network JSON is parsed defensively (validate shape; reject malformed) — no code
  execution from imported data.

## 7. QA Checklist (pm-qa)

- [ ] `npm install` succeeds from clean.
- [ ] `npx tsc --noEmit` passes (no type errors).
- [ ] `npx vitest run` — all tests green.
- [ ] BN test asserts `P(Burglary|JohnCalls,MaryCalls) ≈ 0.284` (±1e-3).
- [ ] HMM test asserts Lab 8 Forward probability and Viterbi path.
- [ ] `npm run build` produces renderer + main bundles with `base: './'`.
- [ ] `npm run dist` attempted; report whether `release/xCalculator.exe` was produced (note if
      electron-builder binary download is blocked by the environment).
- [ ] No `eval`; Electron `contextIsolation` on, `nodeIntegration` off.
- [ ] All four tabs render and are interactive (manual/headless check where feasible).
- [ ] `DOCUMENT.md` present in every directory that received files.
- [ ] Matches spec behavior (§3–§6).

## 8. Test Plan (functional)

- Calculator: `2+3*4=14`, `(2+3)*4=20`, `2^10=1024`, divide-by-zero shows error, keyboard entry.
- Probability: `nCr(5,2)=10`, `nPr(5,2)=20`, `6!=720`, a worked Bayes case; out-of-range flagged.
- Bayes: load Alarm preset → query returns ≈0.284; add a node + drag an edge; cycle rejected;
  CPT row-sum validation fires; export/import round-trips.
- HMM: load Lab 8 preset → Forward prob + Viterbi path match; α/δ/backpointer tables render;
  bad row sums flagged.

## 9. Diff Checklist (pm-reviewer)

- New code matches §1 scope — no scope creep (no extra algorithms/tabs).
- Math lives in `src/lib/**` and is framework-free; UI contains no probability logic.
- No `eval`; Electron security flags correct; Vite `base: './'`.
- Disjoint file ownership respected; configs/`App.tsx`/`package.json` untouched by Phase 2.
- Tests are real assertions against known values, not tautologies.
- Diff is the minimum needed to satisfy the feature.
