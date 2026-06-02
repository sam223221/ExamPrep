/**
 * CptTable — editable conditional probability table for one Bayesian-network
 * node.
 *
 * Rows = the Cartesian product of the parents' states (one row labelled
 * "(no parents)" for roots). Columns = this node's own states. Each cell is an
 * editable probability in [0, 1]; each row must sum to 1. Rows that do not are
 * highlighted with their current sum and offer a "normalize row" button.
 *
 * Holds no inference logic — it only edits the CPT object and reports changes
 * upward. The Cartesian product and key encoding come from the shared types.
 */

import { useState } from 'react';
import { type Cpt, cptKey } from '../../lib/bayes/types';
import { type ParentInfo } from './BayesNode';

interface CptTableProps {
  /** This node's own states (column order). */
  states: string[];
  /** This node's parents, in CPT-key order. */
  parents: ParentInfo[];
  /** The current CPT. */
  cpt: Cpt;
  /** Called with the full updated CPT after an edit or normalize. */
  onChange: (next: Cpt) => void;
}

/** Cartesian product of each parent's states, in parent order. */
function parentCombinations(parents: ParentInfo[]): string[][] {
  if (parents.length === 0) return [[]];
  return parents.reduce<string[][]>(
    (acc, parent) =>
      acc.flatMap((prefix) => parent.states.map((state) => [...prefix, state])),
    [[]],
  );
}

const TOLERANCE = 1e-6;

/** Display form of a committed probability: trims float noise to 6 dp, no trailing zeros. */
function formatCellValue(value: number): string {
  return Number(value.toFixed(6)).toString();
}

interface CptCellProps {
  /** The committed probability for this cell (already clamped to [0, 1]). */
  value: number;
  /** Accessible label, e.g. `P(true | rain)`. */
  ariaLabel: string;
  /** Commit a freshly typed string upward (parsing/clamping is the parent's job). */
  onCommit: (raw: string) => void;
}

/**
 * A single probability input. While focused it shows the user's raw keystrokes
 * (`draft`) so typing a long decimal like `0.1234567` is never truncated
 * mid-entry; on blur it commits the value and reverts to the normalized display
 * form. When not editing, it stays in sync with the committed `value` prop.
 */
function CptCell({ value, ariaLabel, onCommit }: CptCellProps) {
  const [draft, setDraft] = useState<string | null>(null);

  const display = draft ?? formatCellValue(value);

  return (
    <input
      type="number"
      inputMode="decimal"
      min={0}
      max={1}
      step={0.01}
      value={display}
      onChange={(e) => {
        const raw = e.target.value;
        setDraft(raw);
        // Commit live so the row-sum (Σ) indicator stays accurate as you type;
        // the local draft preserves the exact characters typed for display.
        onCommit(raw);
      }}
      onBlur={() => {
        // Drop the draft so the cell snaps back to the normalized committed value.
        setDraft(null);
      }}
      aria-label={ariaLabel}
      className="nodrag w-16 bg-surface-raised px-1.5 py-1 text-center font-mono text-ink outline-none focus:bg-base focus:ring-2 focus:ring-inset focus:ring-accent"
    />
  );
}

export default function CptTable({
  states,
  parents,
  cpt,
  onChange,
}: CptTableProps) {
  const combos = parentCombinations(parents);

  function setCell(key: string, colIndex: number, raw: string) {
    const parsed = raw === '' ? 0 : Number(raw);
    const clamped = Number.isFinite(parsed)
      ? Math.min(1, Math.max(0, parsed))
      : 0;
    const existing = cpt[key] ?? states.map(() => 0);
    const nextRow = existing.map((v, i) => (i === colIndex ? clamped : v));
    onChange({ ...cpt, [key]: nextRow });
  }

  function normalizeRow(key: string) {
    const row = cpt[key] ?? states.map(() => 0);
    const sum = row.reduce((acc, v) => acc + v, 0);
    const nextRow =
      sum > 0
        ? row.map((v) => v / sum)
        : states.map(() => 1 / states.length);
    onChange({ ...cpt, [key]: nextRow });
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-xs">
        <thead>
          <tr>
            {parents.map((parent) => (
              <th
                key={parent.id}
                scope="col"
                className="border border-border bg-surface px-2 py-1 text-left font-medium text-ink-muted"
              >
                {parent.name}
              </th>
            ))}
            {parents.length === 0 && (
              <th
                scope="col"
                className="border border-border bg-surface px-2 py-1 text-left font-medium text-ink-muted"
              >
                (no parents)
              </th>
            )}
            {states.map((state) => (
              <th
                key={state}
                scope="col"
                className="border border-border bg-surface px-2 py-1 text-center font-semibold text-ink"
              >
                {state}
              </th>
            ))}
            <th
              scope="col"
              className="border border-border bg-surface px-2 py-1 text-center font-medium text-ink-muted"
            >
              Σ
            </th>
          </tr>
        </thead>
        <tbody>
          {combos.map((combo) => {
            const key = cptKey(combo);
            const row = cpt[key] ?? states.map(() => 1 / states.length);
            const sum = row.reduce((acc, v) => acc + v, 0);
            const offTarget = Math.abs(sum - 1) > TOLERANCE;
            return (
              <tr key={key || '__root__'}>
                {parents.length === 0 ? (
                  <td className="border border-border bg-surface px-2 py-1 italic text-ink-muted">
                    (no parents)
                  </td>
                ) : (
                  combo.map((value, i) => (
                    <td
                      key={i}
                      className="border border-border bg-surface px-2 py-1 font-mono text-ink"
                    >
                      {value}
                    </td>
                  ))
                )}
                {states.map((state, ci) => (
                  <td key={state} className="border border-border p-0">
                    <CptCell
                      value={row[ci] ?? 0}
                      ariaLabel={`P(${state}${
                        combo.length ? ` | ${combo.join(', ')}` : ''
                      })`}
                      onCommit={(raw) => setCell(key, ci, raw)}
                    />
                  </td>
                ))}
                <td
                  className={[
                    'border border-border px-1.5 py-1 text-center font-mono tabular-nums',
                    offTarget
                      ? 'bg-red-500/15 font-semibold text-red-300'
                      : 'text-ink-muted',
                  ].join(' ')}
                >
                  <span className="mr-1">{sum.toFixed(2)}</span>
                  {offTarget && (
                    <button
                      type="button"
                      onClick={() => normalizeRow(key)}
                      className="nodrag rounded border border-border px-1 text-[10px] text-accent transition-colors hover:bg-surface-raised"
                    >
                      fix
                    </button>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
