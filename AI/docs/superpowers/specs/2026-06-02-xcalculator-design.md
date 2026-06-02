# xCalculator — Design Spec

**Date:** 2026-06-02
**Status:** Approved (design); pending implementation plan
**Location:** `AI/xCalculator/`

## 1. Purpose

A desktop study tool for the AI exam covering probability, Bayesian networks, and
Hidden Markov Models. It bundles four calculators behind one app:

1. A normal arithmetic calculator.
2. A probability calculator (combinatorics + Bayes' theorem).
3. A visual Bayesian-network editor with drag-to-connect nodes, editable CPTs, and
   exact inference.
4. A Hidden Markov Model calculator (Forward + Viterbi) with step-by-step trellis tables.

The app ships as a **portable Windows `.exe`** (double-click, no install, runs offline).

### Success criteria

- Each module produces answers that match hand calculations and the course lab examples.
- The Bayesian-network tab lets the user build a network by typing node names and
  dragging arrows between nodes, fill in CPT tables, and query `P(query | evidence)`.
- The HMM tab reproduces the Lab 8 ice-cream example's Forward probability and Viterbi path.
- `npm run dist` produces a single portable `.exe` that launches the app.

### Out of scope (YAGNI)

- Bayesian-network learning / parameter estimation.
- HMM Backward, smoothing, or Baum-Welch (Forward + Viterbi only).
- Continuous distributions and Normal/Binomial/Poisson tables (combinatorics + Bayes only).
- Cloud sync, multi-user, or any network features. The app is fully offline.

## 2. Stack & architecture

- **UI:** React 18 + TypeScript, built with Vite.
- **Styling:** Tailwind CSS v4 via the `@tailwindcss/vite` plugin.
- **Graph editor:** React Flow (`@xyflow/react` v12) for the Bayesian-network canvas.
- **Desktop shell:** Electron, with `electron-vite` for dev/build and `electron-builder`
  for packaging (Windows `portable` target, x64).
- **Tests:** Vitest, exercising the pure math modules.

**Design principle:** all algorithms live in framework-free TypeScript modules under
`src/lib/`. UI components call into these modules but contain no probability logic. This
keeps every algorithm independently testable and verifiable.

### Directory layout

```
xCalculator/
  package.json
  vite.config.ts            # base: './' so file:// loading works in Electron
  electron.vite.config.ts   # main / preload / renderer config (or vite-plugin-electron)
  tsconfig.json
  index.html
  electron/
    main.ts                 # creates BrowserWindow, loads built renderer
    preload.ts
  electron-builder.yml      # win portable target -> release/xCalculator.exe
  src/
    main.tsx                # React entry
    App.tsx                 # tab shell + active-tab state
    index.css               # Tailwind import + theme tokens
    components/
      Tabs.tsx
      calculator/Calculator.tsx
      probability/Probability.tsx
      bayes/
        BayesNetwork.tsx     # React Flow canvas + toolbar
        BayesNode.tsx        # custom node: name, states, CPT entry
        CptTable.tsx         # CPT editor with row-sum validation
        QueryPanel.tsx       # query var + evidence + results
      hmm/
        Hmm.tsx
        MatrixEditor.tsx     # reusable editable numeric grid
        TrellisTable.tsx     # alpha / delta / backpointer display
    lib/
      calc.ts                # shunting-yard expression evaluator
      probability.ts         # factorial, nPr, nCr, prob rules, Bayes
      bayes/
        types.ts             # BNNode, BNEdge, CPT types
        inference.ts         # enumeration-ask exact inference
      hmm/
        types.ts             # HMMModel type
        forward.ts           # Forward algorithm + alpha trellis
        viterbi.ts           # Viterbi best path + delta/backpointer
    lib/__tests__/
      probability.test.ts
      bayes.test.ts
      hmm.test.ts
  README.md
```

## 3. Module — Normal calculator

- Button grid: digits, `.`, `+ − × ÷`, `^`, parentheses, `%`, `±`, `=`, `C` (clear),
  `⌫` (backspace).
- Full keyboard input mirrors the buttons; `Enter` evaluates, `Esc` clears.
- Expression is evaluated by a **shunting-yard parser** in `lib/calc.ts` (never `eval`).
  Supports `+ - * / ^`, unary minus, and parentheses with standard precedence.
- A running history list shows recent `expression = result` entries; clicking one reloads it.
- Division by zero and malformed input surface a friendly inline error, not a crash.

## 4. Module — Probability

Each tool is a labelled form: inputs, a computed result, and the formula displayed.

- **Combinatorics:** `n!`, permutations `nPr = n!/(n−r)!`, combinations `nCr = n!/(r!(n−r)!)`.
  Guard against `r > n` and negatives with inline validation. Uses an exact integer/BigInt
  path for factorials to avoid float drift on large `n`.
- **Probability rules:**
  - Complement: `P(¬A) = 1 − P(A)`
  - Union: `P(A∪B) = P(A) + P(B) − P(A∩B)`
  - Intersection (independent): `P(A∩B) = P(A)·P(B)`
  - Conditional: `P(A|B) = P(A∩B) / P(B)`
- **Bayes' theorem** (total-probability form):
  `P(A|B) = P(B|A)P(A) / [ P(B|A)P(A) + P(B|¬A)P(¬A) ]`
  Inputs: `P(A)`, `P(B|A)`, `P(B|¬A)`. Output: `P(A|B)`, with intermediate terms shown.
- All probability inputs validated to `[0, 1]`; out-of-range values flagged inline.

## 5. Module — Bayesian Network

### Editor (React Flow)

- **Add node:** toolbar button or double-click on empty canvas. New node gets a unique
  default name and the states `["true", "false"]`.
- **Edit node:** rename; edit the list of states (add/remove, rename). Minimum two states.
- **Connect:** drag from a node's source handle to another node's target handle to create a
  directed `parent → child` edge. A connection that would create a cycle is rejected with a
  toast/inline message (the network must remain a DAG).
- **Delete:** remove nodes and edges; deleting an edge or node rebuilds affected CPTs.

### CPT table per node (`CptTable.tsx`)

- Rows = the Cartesian product of all parent states (one row per parent-state combination;
  a single row labelled "(no parents)" for roots). Columns = this node's own states.
- Each cell is an editable probability in `[0, 1]`. Each **row must sum to 1**; rows that
  don't are highlighted with the current sum shown. A "normalize row" helper is available.
- When a node gains/loses a parent or a parent's states change, the CPT is rebuilt,
  preserving existing values where the row/column still applies and defaulting new cells to
  a uniform distribution.

### Inference (`lib/bayes/inference.ts`)

- **Exact inference by enumeration** (AIMA `ENUMERATION-ASK`): given a query variable `X`
  and an evidence assignment `e` over any subset of other variables, compute the full
  distribution `P(X | e)` by summing the joint over all hidden-variable assignments in
  topological order, then normalizing.
- Supports multi-valued discrete variables and arbitrary evidence. Exponential in the number
  of hidden variables, which is fine for exam-sized networks.
- Also exposes: marginal `P(X)` (enumeration with empty evidence) and full-joint lookup for a
  complete assignment `P(x1, …, xn) = Π P(xi | parents(xi))`.

### Query panel (`QueryPanel.tsx`)

- Select query variable; set evidence by choosing a value (or "unset") for each other node.
- Shows the resulting distribution over the query variable's states as a bar + numeric table.
- Live recompute on edits; clear "network invalid" message when CPTs don't sum to 1 or the
  graph isn't a connected DAG.

### Presets & persistence

- Built-in **Alarm/Burglary** example network (AIMA) loadable from the toolbar.
- Export the current network to a JSON file and import it back, so practice networks persist
  between sessions. Auto-save the working network to `localStorage`.

## 6. Module — HMM

### Inputs

- **Hidden states** list (e.g., `hot`, `cold`).
- **Observation symbols** list (e.g., `1`, `2`, `3`).
- **Start probabilities π** (one per state; should sum to 1).
- **End probabilities** (optional, one per state). If left blank, termination probability is
  treated as 1 for every state (standard textbook Forward without an explicit end state).
- **Transition matrix A** (states × states), each row summing to 1.
- **Emission matrix B** (states × symbols), each row summing to 1.
- **Observation sequence** (a list of symbols).

Matrices are edited via a reusable `MatrixEditor` grid with per-row sum validation.

### Algorithms

- **Forward** (`lib/hmm/forward.ts`): computes `P(O | model)` and returns the full `α` trellis
  (states × timesteps). `α_t(j) = [ Σ_i α_{t−1}(i) · a_{ij} ] · b_j(o_t)`, initialized from π,
  terminated by summing (optionally weighting by end probabilities).
- **Viterbi** (`lib/hmm/viterbi.ts`): computes the most-likely hidden-state path and returns the
  `δ` (best-score) trellis and the `backpointer` matrix. Path recovered by following
  backpointers from the best terminal state.

### Display (`TrellisTable.tsx`)

- Forward tab: the `α` table with the final `P(O)` highlighted.
- Viterbi tab: the `δ` table, the backpointer table, and the recovered best path of state names.
- Built-in **Lab 8 ice-cream preset** (states hot/cold; symbols 1/2/3; the Lab 8 transition and
  emission numbers) so the user can confirm the tool matches the course example.

## 7. Correctness strategy (Vitest)

- `probability.test.ts`: `nCr(5,2)=10`, `nPr(5,2)=20`, `factorial(6)=720`, a worked Bayes case.
- `bayes.test.ts`: build the AIMA Alarm network in code; assert
  `P(Burglary=true | JohnCalls=true, MaryCalls=true) ≈ 0.284` (±1e-3); assert marginals and a
  full-joint value against hand computation.
- `hmm.test.ts`: build the Lab 8 ice-cream model; assert the Forward probability for an
  observation set and the Viterbi path match the known result.

## 8. Build, run, packaging

Prerequisite: **Node.js** installed (LTS).

- `npm install` — install dependencies.
- `npm run dev` — launch the app in an Electron window with hot reload (renderer via Vite).
- `npm run build` — type-check (`tsc`) and produce the renderer + main bundles.
- `npm run test` — run the Vitest suite.
- `npm run dist` — build then run `electron-builder --win portable`, producing
  `release/xCalculator.exe` — a single portable executable (~100–150 MB, bundles Chromium),
  double-clickable, runs offline.

`README.md` documents all of the above plus a short "what each tab does" section.

## 9. Risks & notes

- **Vite `base`** must be `'./'` (relative) so the packaged app loads assets over `file://`.
- **React Flow** is `@xyflow/react` v12 — verify current API for custom nodes, handles, and
  connection validation during implementation (use Context7).
- **Tailwind v4** uses the Vite plugin + `@import "tailwindcss"`; no `tailwind.config.js`
  required by default — verify setup during implementation.
- **Enumeration** is exponential; acceptable for exam-sized nets. No need for variable
  elimination given scope.
- Portable `.exe` size is inherent to Electron; acceptable per the chosen packaging option.
