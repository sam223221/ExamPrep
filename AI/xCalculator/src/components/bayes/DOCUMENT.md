# `src/components/bayes` — Bayesian Network tab UI

React UI for the Bayesian-network tab: a React Flow (`@xyflow/react` v12) canvas
plus a live query panel. **No inference logic lives here** — all math is
delegated to `src/lib/bayes`.

## Files

- **`BayesNetwork.tsx`** — the tab orchestrator (default export, no props,
  wrapped in `ReactFlowProvider`). Owns the graph state (`useState` of nodes +
  edges), CPT bookkeeping, persistence and import/export. Toolbar: **Add node**
  (also double-click canvas), **Load Alarm example**, **Export JSON**,
  **Import JSON**, **Clear**.
- **`BayesNode.tsx`** — custom React Flow node (`nodeTypes = { bayes }`). Editable
  name, state list (add/remove/rename, min 2), embedded CPT editor, and a target
  Handle (top) + source Handle (bottom). Mutates graph state through callbacks
  carried on `node.data`.
- **`CptTable.tsx`** — CPT editor. Rows = Cartesian product of parents' states
  (a single "(no parents)" row for roots); columns = the node's states. Cells
  clamp to `[0, 1]`; each row shows its sum, highlights when it is not 1, and
  offers a "fix" (normalize) button. Each cell is a small internal `CptCell`
  component that holds the raw typed string in local `draft` state while focused
  and reverts to the normalized committed value on blur, so typing a long
  decimal (e.g. a 7th digit) is not truncated on each keystroke. The `ParentInfo`
  type is imported from `BayesNode.tsx` (single source of truth), not redeclared.
- **`QueryPanel.tsx`** — pick the query variable, set evidence (value or
  "unset") for every other node, and see `P(query | evidence)` as a numeric +
  bar display. Recomputes live; shows a clear message when the network is not a
  DAG or its CPTs do not sum to 1.

## Key decisions

- **Single source of truth = the React Flow graph.** A node's `parents` are
  derived from edges (`resolveParents`); the pure model is built on demand via
  `toModel`. Inference runs against that model.
- **DAG invariant.** `isValidConnection` walks the existing graph with
  `getOutgoers` (DFS from the prospective target) to reject any edge that would
  create a cycle; `onConnect` re-checks and shows a toast. Self-loops and
  duplicate edges are also rejected.
- **CPT rebuild.** Whenever edges or a node's states change, `rebuildCpt`
  regenerates the affected CPTs, preserving values for rows/columns that still
  apply and defaulting new cells to uniform.
- **Persistence.** The working network auto-saves to `localStorage`
  (`xcalculator.bayes.network.v1`) and is restored on mount. Export downloads a
  versioned JSON; import is parsed defensively (`parseSerialNetwork` validates
  shape and rejects malformed input — no code execution).
- The Alarm preset numbers match `src/lib/__tests__/bayes.test.ts`, so loading
  it and querying `Burglary` with `JohnCalls=true, MaryCalls=true` yields
  ≈ 0.284.

## React Flow v12 API used

`ReactFlow`, `ReactFlowProvider`, `Background`, `Controls`, `MiniMap`, `Handle`,
`Position`, `addEdge`, `applyNodeChanges`, `applyEdgeChanges`, `getOutgoers`,
`useNodesState`-style local state, `isValidConnection`, custom `nodeTypes`, and
the required `import '@xyflow/react/dist/style.css'`.

## Connections

Imported by `src/App.tsx` as the `bayes` tab panel (shell owned by setup; not
modified here).
