/**
 * BayesNode — a custom React Flow node representing one Bayesian-network
 * variable.
 *
 * Shows the (editable) node name, its states (add / remove / rename, minimum
 * two), and an embedded CPT editor. Exposes a target Handle (top, for incoming
 * parent edges) and a source Handle (bottom, for outgoing child edges).
 *
 * All graph state lives in the parent `BayesNetwork` component; this node reads
 * and mutates it through callbacks carried on `data`. It contains no inference
 * logic.
 */

import { useState } from 'react';
import { Handle, Position, type NodeProps, type Node } from '@xyflow/react';
import CptTable from './CptTable';
import { type Cpt } from '../../lib/bayes/types';

/** Parent info supplied to the node so the CPT table can label its rows. */
export interface ParentInfo {
  id: string;
  name: string;
  states: string[];
}

/** Data carried by every Bayesian-network node in the React Flow graph. */
export interface BayesNodeData {
  name: string;
  states: string[];
  cpt: Cpt;
  /** Resolved parent info (derived from edges by the parent component). */
  parents: ParentInfo[];
  /** Mutation callbacks wired by the parent component. */
  onRename: (id: string, name: string) => void;
  onStatesChange: (id: string, states: string[]) => void;
  onCptChange: (id: string, cpt: Cpt) => void;
  onDelete: (id: string) => void;
  [key: string]: unknown;
}

export type BayesFlowNode = Node<BayesNodeData, 'bayes'>;

export default function BayesNode({ id, data, selected }: NodeProps<BayesFlowNode>) {
  const [open, setOpen] = useState(true);
  const { name, states, cpt, parents } = data;

  function renameState(index: number, value: string) {
    data.onStatesChange(
      id,
      states.map((s, i) => (i === index ? value : s)),
    );
  }

  function addState() {
    data.onStatesChange(id, [...states, `state${states.length + 1}`]);
  }

  function removeState(index: number) {
    if (states.length <= 2) return;
    data.onStatesChange(
      id,
      states.filter((_, i) => i !== index),
    );
  }

  return (
    <div
      className={[
        'min-w-[15rem] max-w-xs rounded-xl border bg-surface shadow-lg transition-colors',
        selected ? 'border-accent' : 'border-border',
      ].join(' ')}
    >
      <Handle
        type="target"
        position={Position.Top}
        className="!h-3 !w-3 !border-2 !border-surface !bg-ink-muted"
        aria-label={`${name} incoming connection`}
      />

      <header className="flex items-center gap-2 border-b border-border px-3 py-2">
        <input
          value={name}
          onChange={(e) => data.onRename(id, e.target.value)}
          aria-label="Node name"
          className="nodrag min-w-0 flex-1 rounded bg-transparent px-1 py-0.5 text-sm font-semibold text-ink outline-none focus:bg-surface-raised focus:ring-2 focus:ring-accent"
        />
        <button
          type="button"
          onClick={() => setOpen((o) => !o)}
          aria-expanded={open}
          aria-label={open ? 'Collapse CPT' : 'Expand CPT'}
          className="nodrag rounded border border-border px-1.5 py-0.5 text-xs text-ink-muted transition-colors hover:text-ink"
        >
          {open ? '−' : '+'}
        </button>
        <button
          type="button"
          onClick={() => data.onDelete(id)}
          aria-label={`Delete node ${name}`}
          className="nodrag rounded border border-border px-1.5 py-0.5 text-xs text-ink-muted transition-colors hover:text-red-300"
        >
          ✕
        </button>
      </header>

      {open && (
        <div className="flex flex-col gap-3 p-3">
          <div>
            <div className="mb-1 flex items-center justify-between">
              <span className="text-xs font-medium uppercase tracking-wide text-ink-muted">
                States
              </span>
              <button
                type="button"
                onClick={addState}
                className="nodrag rounded border border-border px-1.5 py-0.5 text-[11px] text-accent transition-colors hover:bg-surface-raised"
              >
                + add
              </button>
            </div>
            <ul className="flex flex-col gap-1">
              {states.map((state, i) => (
                <li key={i} className="flex items-center gap-1">
                  <input
                    value={state}
                    onChange={(e) => renameState(i, e.target.value)}
                    aria-label={`State ${i + 1} of ${name}`}
                    className="nodrag min-w-0 flex-1 rounded border border-border bg-surface-raised px-2 py-1 font-mono text-xs text-ink outline-none focus:ring-2 focus:ring-accent"
                  />
                  <button
                    type="button"
                    onClick={() => removeState(i)}
                    disabled={states.length <= 2}
                    aria-label={`Remove state ${state}`}
                    className="nodrag rounded border border-border px-1.5 py-1 text-[11px] text-ink-muted transition-colors hover:text-red-300 disabled:cursor-not-allowed disabled:opacity-40"
                  >
                    ✕
                  </button>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <span className="mb-1 block text-xs font-medium uppercase tracking-wide text-ink-muted">
              CPT
            </span>
            <CptTable
              states={states}
              parents={parents}
              cpt={cpt}
              onChange={(next) => data.onCptChange(id, next)}
            />
          </div>
        </div>
      )}

      <Handle
        type="source"
        position={Position.Bottom}
        className="!h-3 !w-3 !border-2 !border-surface !bg-accent"
        aria-label={`${name} outgoing connection`}
      />
    </div>
  );
}
