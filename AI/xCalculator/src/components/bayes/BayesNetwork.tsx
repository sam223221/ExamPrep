/**
 * BayesNetwork — the Bayesian-network tab.
 *
 * A React Flow canvas for building a discrete Bayesian network by adding nodes
 * and dragging parent -> child edges, with per-node editable CPTs and a live
 * query panel. Inference is delegated to `src/lib/bayes/inference`; this file
 * owns only the graph state, CPT bookkeeping, persistence, and import/export.
 *
 * Invariants enforced here:
 *   - The graph stays a DAG: a connection that would create a cycle is rejected
 *     (both proactively via `isValidConnection` and defensively in `onConnect`).
 *   - A node's CPT always matches its current parents and states: whenever an
 *     edge or a state list changes, affected CPTs are rebuilt, preserving values
 *     for rows/columns that still apply and defaulting new cells to uniform.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  ReactFlow,
  ReactFlowProvider,
  Background,
  Controls,
  MiniMap,
  addEdge,
  applyNodeChanges,
  applyEdgeChanges,
  getOutgoers,
  type Edge,
  type Connection,
  type NodeChange,
  type EdgeChange,
  type IsValidConnection,
  type NodeTypes,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import BayesNode, {
  type BayesFlowNode,
  type BayesNodeData,
  type ParentInfo,
} from './BayesNode';
import QueryPanel from './QueryPanel';
import {
  type BayesNetworkModel,
  type BNNode,
  type Cpt,
  cptKey,
} from '../../lib/bayes/types';

const STORAGE_KEY = 'xcalculator.bayes.network.v1';
const nodeTypes: NodeTypes = { bayes: BayesNode };

// --- CPT bookkeeping ---------------------------------------------------------

/** Cartesian product of each parent's state list, in parent order. */
function parentCombinations(parents: ParentInfo[]): string[][] {
  if (parents.length === 0) return [[]];
  return parents.reduce<string[][]>(
    (acc, parent) =>
      acc.flatMap((prefix) => parent.states.map((state) => [...prefix, state])),
    [[]],
  );
}

/**
 * Rebuild a CPT for the given parents and states, preserving any existing row
 * that still has a valid key and defaulting new cells to a uniform distribution.
 */
function rebuildCpt(
  previous: Cpt,
  parents: ParentInfo[],
  states: string[],
): Cpt {
  const uniform = states.map(() => 1 / states.length);
  const next: Cpt = {};
  for (const combo of parentCombinations(parents)) {
    const key = cptKey(combo);
    const old = previous[key];
    if (old && old.length === states.length) {
      next[key] = [...old];
    } else if (old && old.length > 0) {
      // States changed: keep overlapping columns, fill the rest uniformly.
      next[key] = states.map((_, i) => old[i] ?? 1 / states.length);
    } else {
      next[key] = [...uniform];
    }
  }
  return next;
}

// --- model <-> flow conversion ----------------------------------------------

/** Resolve the ParentInfo list for a node from the current edges. */
function resolveParents(
  nodeId: string,
  nodes: BayesFlowNode[],
  edges: Edge[],
): ParentInfo[] {
  const byId = new Map(nodes.map((n) => [n.id, n]));
  return edges
    .filter((e) => e.target === nodeId)
    .map((e) => byId.get(e.source))
    .filter((n): n is BayesFlowNode => Boolean(n))
    .map((n) => ({ id: n.id, name: n.data.name, states: n.data.states }));
}

/** Build the pure-inference model from the current flow graph. */
function toModel(nodes: BayesFlowNode[], edges: Edge[]): BayesNetworkModel {
  return {
    nodes: nodes.map<BNNode>((n) => ({
      id: n.id,
      name: n.data.name,
      states: n.data.states,
      parents: edges
        .filter((e) => e.target === n.id)
        .map((e) => e.source),
      cpt: n.data.cpt,
    })),
  };
}

// --- presets / serialisation -------------------------------------------------

interface SerialNode {
  id: string;
  name: string;
  states: string[];
  cpt: Cpt;
  position: { x: number; y: number };
}
interface SerialEdge {
  id: string;
  source: string;
  target: string;
}
interface SerialNetwork {
  version: 1;
  nodes: SerialNode[];
  edges: SerialEdge[];
}

/** The AIMA Alarm preset, built directly as flow nodes + edges. */
function alarmPreset(): { nodes: BayesFlowNode[]; edges: Edge[] } {
  const mk = (
    id: string,
    states: string[],
    cpt: Cpt,
    position: { x: number; y: number },
  ): BayesFlowNode => ({
    id,
    type: 'bayes',
    position,
    data: {
      name: id,
      states,
      cpt,
      parents: [],
      onRename: () => {},
      onStatesChange: () => {},
      onCptChange: () => {},
      onDelete: () => {},
    },
  });
  const TF = ['true', 'false'];
  const nodes: BayesFlowNode[] = [
    mk('Burglary', [...TF], { [cptKey([])]: [0.001, 0.999] }, { x: 80, y: 20 }),
    mk('Earthquake', [...TF], { [cptKey([])]: [0.002, 0.998] }, { x: 460, y: 20 }),
    mk(
      'Alarm',
      [...TF],
      {
        [cptKey(['true', 'true'])]: [0.95, 0.05],
        [cptKey(['true', 'false'])]: [0.94, 0.06],
        [cptKey(['false', 'true'])]: [0.29, 0.71],
        [cptKey(['false', 'false'])]: [0.001, 0.999],
      },
      { x: 270, y: 320 },
    ),
    mk(
      'JohnCalls',
      [...TF],
      {
        [cptKey(['true'])]: [0.9, 0.1],
        [cptKey(['false'])]: [0.05, 0.95],
      },
      { x: 80, y: 620 },
    ),
    mk(
      'MaryCalls',
      [...TF],
      {
        [cptKey(['true'])]: [0.7, 0.3],
        [cptKey(['false'])]: [0.01, 0.99],
      },
      { x: 460, y: 620 },
    ),
  ];
  const edges: Edge[] = [
    { id: 'Burglary->Alarm', source: 'Burglary', target: 'Alarm' },
    { id: 'Earthquake->Alarm', source: 'Earthquake', target: 'Alarm' },
    { id: 'Alarm->JohnCalls', source: 'Alarm', target: 'JohnCalls' },
    { id: 'Alarm->MaryCalls', source: 'Alarm', target: 'MaryCalls' },
  ];
  return { nodes, edges };
}

/**
 * Defensively parse an imported network. Validates the shape and rejects
 * anything malformed; never executes imported data. Returns `null` on failure.
 */
function parseSerialNetwork(raw: unknown): SerialNetwork | null {
  if (typeof raw !== 'object' || raw === null) return null;
  const obj = raw as Record<string, unknown>;
  if (obj.version !== 1) return null;
  if (!Array.isArray(obj.nodes) || !Array.isArray(obj.edges)) return null;

  const nodes: SerialNode[] = [];
  for (const n of obj.nodes) {
    if (typeof n !== 'object' || n === null) return null;
    const node = n as Record<string, unknown>;
    if (typeof node.id !== 'string' || node.id.length === 0) return null;
    if (typeof node.name !== 'string') return null;
    if (
      !Array.isArray(node.states) ||
      node.states.length < 2 ||
      !node.states.every((s) => typeof s === 'string')
    ) {
      return null;
    }
    if (typeof node.cpt !== 'object' || node.cpt === null) return null;
    const cpt: Cpt = {};
    for (const [key, value] of Object.entries(node.cpt as Record<string, unknown>)) {
      if (!Array.isArray(value) || !value.every((v) => typeof v === 'number')) {
        return null;
      }
      cpt[key] = value as number[];
    }
    const pos = node.position as Record<string, unknown> | undefined;
    const position =
      pos && typeof pos.x === 'number' && typeof pos.y === 'number'
        ? { x: pos.x, y: pos.y }
        : { x: 0, y: 0 };
    nodes.push({
      id: node.id,
      name: node.name,
      states: node.states as string[],
      cpt,
      position,
    });
  }

  const ids = new Set(nodes.map((n) => n.id));
  const edges: SerialEdge[] = [];
  for (const e of obj.edges) {
    if (typeof e !== 'object' || e === null) return null;
    const edge = e as Record<string, unknown>;
    if (
      typeof edge.source !== 'string' ||
      typeof edge.target !== 'string' ||
      !ids.has(edge.source) ||
      !ids.has(edge.target)
    ) {
      return null;
    }
    edges.push({
      id: typeof edge.id === 'string' ? edge.id : `${edge.source}->${edge.target}`,
      source: edge.source,
      target: edge.target,
    });
  }

  return { version: 1, nodes, edges };
}

function serialToFlow(serial: SerialNetwork): {
  nodes: BayesFlowNode[];
  edges: Edge[];
} {
  const nodes: BayesFlowNode[] = serial.nodes.map((n) => ({
    id: n.id,
    type: 'bayes',
    position: n.position,
    data: {
      name: n.name,
      states: n.states,
      cpt: n.cpt,
      parents: [],
      onRename: () => {},
      onStatesChange: () => {},
      onCptChange: () => {},
      onDelete: () => {},
    },
  }));
  const edges: Edge[] = serial.edges.map((e) => ({
    id: e.id,
    source: e.source,
    target: e.target,
  }));
  return { nodes, edges };
}

// --- component ---------------------------------------------------------------

function BayesNetworkInner() {
  const [nodes, setNodes] = useState<BayesFlowNode[]>(() => alarmPreset().nodes);
  const [edges, setEdges] = useState<Edge[]>(() => alarmPreset().edges);
  const [toast, setToast] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const idCounter = useRef(1);
  const hydrated = useRef(false);

  function flash(message: string) {
    setToast(message);
    window.setTimeout(() => setToast(null), 2500);
  }

  // Load any autosaved network once on mount.
  useEffect(() => {
    if (hydrated.current) return;
    hydrated.current = true;
    try {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (!stored) return;
      const parsed = parseSerialNetwork(JSON.parse(stored));
      if (parsed && parsed.nodes.length > 0) {
        const flow = serialToFlow(parsed);
        setNodes(flow.nodes);
        setEdges(flow.edges);
      }
    } catch {
      // Corrupt storage — ignore and keep the default preset.
    }
  }, []);

  // Autosave on every change (after hydration).
  useEffect(() => {
    if (!hydrated.current) return;
    const serial: SerialNetwork = {
      version: 1,
      nodes: nodes.map((n) => ({
        id: n.id,
        name: n.data.name,
        states: n.data.states,
        cpt: n.data.cpt,
        position: n.position,
      })),
      edges: edges.map((e) => ({ id: e.id, source: e.source, target: e.target })),
    };
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(serial));
    } catch {
      // Storage may be unavailable (private mode / quota); non-fatal.
    }
  }, [nodes, edges]);

  // --- node/edge mutation callbacks -----------------------------------------

  const renameNode = useCallback((id: string, name: string) => {
    setNodes((prev) =>
      prev.map((n) => (n.id === id ? { ...n, data: { ...n.data, name } } : n)),
    );
  }, []);

  const changeStates = useCallback((id: string, states: string[]) => {
    setNodes((prev) => {
      // Update this node's states + CPT, then rebuild children's CPTs since a
      // parent's state list feeds their rows.
      const target = prev.find((n) => n.id === id);
      if (!target) return prev;
      return prev.map((n) => {
        if (n.id === id) {
          const selfParents = n.data.parents;
          return {
            ...n,
            data: {
              ...n.data,
              states,
              cpt: rebuildCpt(n.data.cpt, selfParents, states),
            },
          };
        }
        return n;
      });
    });
  }, []);

  const changeCpt = useCallback((id: string, cpt: Cpt) => {
    setNodes((prev) =>
      prev.map((n) => (n.id === id ? { ...n, data: { ...n.data, cpt } } : n)),
    );
  }, []);

  const deleteNode = useCallback((id: string) => {
    setNodes((prev) => prev.filter((n) => n.id !== id));
    setEdges((prev) => prev.filter((e) => e.source !== id && e.target !== id));
  }, []);

  // --- React Flow change handlers -------------------------------------------

  const onNodesChange = useCallback((changes: NodeChange<BayesFlowNode>[]) => {
    setNodes((prev) => applyNodeChanges(changes, prev));
  }, []);

  const onEdgesChange = useCallback((changes: EdgeChange[]) => {
    setEdges((prev) => applyEdgeChanges(changes, prev));
  }, []);

  // Reject connections that would create a cycle, self-loops, or duplicates.
  const isValidConnection = useCallback<IsValidConnection>(
    (connection) => {
      const { source, target } = connection;
      if (!source || !target) return false;
      if (source === target) return false;
      if (edges.some((e) => e.source === source && e.target === target)) {
        return false;
      }
      // A connection source -> target is a cycle if `source` is reachable from
      // `target` by following existing edges.
      const targetNode = nodes.find((n) => n.id === target);
      if (!targetNode) return false;
      const stack = getOutgoers(targetNode, nodes, edges);
      const seen = new Set<string>();
      while (stack.length > 0) {
        const current = stack.pop()!;
        if (current.id === source) return false;
        if (seen.has(current.id)) continue;
        seen.add(current.id);
        stack.push(...getOutgoers(current, nodes, edges));
      }
      return true;
    },
    [nodes, edges],
  );

  const onConnect = useCallback(
    (connection: Connection) => {
      if (!isValidConnection(connection)) {
        flash('Connection rejected: it would create a cycle or duplicate.');
        return;
      }
      setEdges((prev) =>
        addEdge(
          {
            ...connection,
            id: `${connection.source}->${connection.target}`,
          },
          prev,
        ),
      );
    },
    [isValidConnection],
  );

  // --- toolbar actions ------------------------------------------------------

  const addNode = useCallback(() => {
    setNodes((prev) => {
      let id = `Node${idCounter.current}`;
      const existing = new Set(prev.map((n) => n.id));
      while (existing.has(id)) {
        idCounter.current += 1;
        id = `Node${idCounter.current}`;
      }
      idCounter.current += 1;
      const states = ['true', 'false'];
      const newNode: BayesFlowNode = {
        id,
        type: 'bayes',
        position: {
          x: 120 + (prev.length % 4) * 60,
          y: 120 + prev.length * 30,
        },
        data: {
          name: id,
          states,
          cpt: { [cptKey([])]: [0.5, 0.5] },
          parents: [],
          onRename: () => {},
          onStatesChange: () => {},
          onCptChange: () => {},
          onDelete: () => {},
        },
      };
      return [...prev, newNode];
    });
  }, []);

  // Add a node only when the double-click lands on the empty canvas (the
  // React Flow pane), not on an existing node or control.
  const onPaneDoubleClick = useCallback(
    (event: React.MouseEvent) => {
      const target = event.target as HTMLElement;
      if (target.classList.contains('react-flow__pane')) {
        addNode();
      }
    },
    [addNode],
  );

  const loadAlarm = useCallback(() => {
    const preset = alarmPreset();
    setNodes(preset.nodes);
    setEdges(preset.edges);
    flash('Loaded the AIMA Alarm example.');
  }, []);

  const clearAll = useCallback(() => {
    setNodes([]);
    setEdges([]);
    flash('Cleared the network.');
  }, []);

  const exportJson = useCallback(() => {
    const serial: SerialNetwork = {
      version: 1,
      nodes: nodes.map((n) => ({
        id: n.id,
        name: n.data.name,
        states: n.data.states,
        cpt: n.data.cpt,
        position: n.position,
      })),
      edges: edges.map((e) => ({ id: e.id, source: e.source, target: e.target })),
    };
    const blob = new Blob([JSON.stringify(serial, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'bayes-network.json';
    link.click();
    URL.revokeObjectURL(url);
  }, [nodes, edges]);

  const importJson = useCallback((file: File) => {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const parsed = parseSerialNetwork(JSON.parse(String(reader.result)));
        if (!parsed) {
          flash('Import failed: file is not a valid network.');
          return;
        }
        const flow = serialToFlow(parsed);
        setNodes(flow.nodes);
        setEdges(flow.edges);
        flash('Network imported.');
      } catch {
        flash('Import failed: could not parse JSON.');
      }
    };
    reader.readAsText(file);
  }, []);

  // --- derive display nodes (inject parents + callbacks) --------------------

  const displayNodes = useMemo<BayesFlowNode[]>(() => {
    return nodes.map((n) => {
      const parents = resolveParents(n.id, nodes, edges);
      const data: BayesNodeData = {
        ...n.data,
        parents,
        onRename: renameNode,
        onStatesChange: changeStates,
        onCptChange: changeCpt,
        onDelete: deleteNode,
      };
      return { ...n, data };
    });
  }, [nodes, edges, renameNode, changeStates, changeCpt, deleteNode]);

  // Keep each node's CPT in sync with its parents whenever edges change.
  useEffect(() => {
    setNodes((prev) => {
      let changed = false;
      const next = prev.map((n) => {
        const parents = resolveParents(n.id, prev, edges);
        const rebuilt = rebuildCpt(n.data.cpt, parents, n.data.states);
        const sameKeys =
          Object.keys(rebuilt).length === Object.keys(n.data.cpt).length &&
          Object.keys(rebuilt).every((k) => k in n.data.cpt);
        if (sameKeys) return n;
        changed = true;
        return { ...n, data: { ...n.data, cpt: rebuilt } };
      });
      return changed ? next : prev;
    });
  }, [edges]);

  const model = useMemo(() => toModel(nodes, edges), [nodes, edges]);

  return (
    <div className="flex h-full min-h-0">
      <div className="relative flex min-w-0 flex-1 flex-col">
        <div className="flex flex-wrap items-center gap-2 border-b border-border bg-surface px-4 py-2.5">
          <ToolbarButton onClick={addNode}>Add node</ToolbarButton>
          <ToolbarButton onClick={loadAlarm} variant="ghost">
            Load Alarm example
          </ToolbarButton>
          <ToolbarButton onClick={exportJson} variant="ghost">
            Export JSON
          </ToolbarButton>
          <ToolbarButton
            onClick={() => fileInputRef.current?.click()}
            variant="ghost"
          >
            Import JSON
          </ToolbarButton>
          <ToolbarButton onClick={clearAll} variant="ghost">
            Clear
          </ToolbarButton>
          <input
            ref={fileInputRef}
            type="file"
            accept="application/json,.json"
            className="hidden"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) importJson(file);
              e.target.value = '';
            }}
          />
          <span className="ml-auto text-xs text-ink-muted">
            Drag from the green handle (bottom) to another node's top to add a
            parent → child edge.
          </span>
        </div>

        <div className="relative min-h-0 flex-1">
          <ReactFlow
            nodes={displayNodes}
            edges={edges}
            nodeTypes={nodeTypes}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            isValidConnection={isValidConnection}
            onDoubleClick={onPaneDoubleClick}
            fitView
            proOptions={{ hideAttribution: true }}
            className="bg-base"
          >
            <Background color="#28344a" gap={20} />
            <Controls className="border-border! bg-surface!" />
            <MiniMap
              pannable
              zoomable
              className="border! border-border! bg-surface!"
              maskColor="rgba(11,15,23,0.7)"
              nodeColor="#1b2433"
            />
          </ReactFlow>

          {toast && (
            <div
              role="status"
              className="pointer-events-none absolute bottom-4 left-1/2 -translate-x-1/2 rounded-lg border border-border bg-surface-raised px-4 py-2 text-sm text-ink shadow-lg"
            >
              {toast}
            </div>
          )}
        </div>
      </div>

      <div className="w-80 shrink-0">
        <QueryPanel network={model} />
      </div>
    </div>
  );
}

export default function BayesNetwork() {
  return (
    <ReactFlowProvider>
      <BayesNetworkInner />
    </ReactFlowProvider>
  );
}

// --- toolbar button ----------------------------------------------------------

function ToolbarButton({
  children,
  onClick,
  variant = 'solid',
}: {
  children: React.ReactNode;
  onClick: () => void;
  variant?: 'solid' | 'ghost';
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={[
        'rounded-md px-3 py-1.5 text-sm font-medium transition-colors outline-none focus-visible:ring-2 focus-visible:ring-accent',
        variant === 'solid'
          ? 'bg-accent/15 text-accent hover:bg-accent/25'
          : 'border border-border text-ink-muted hover:bg-surface-raised hover:text-ink',
      ].join(' ')}
    >
      {children}
    </button>
  );
}
