/**
 * HMM tab — Forward (P(O) + α trellis) and Viterbi (best path + δ/backpointer
 * tables) for a discrete Hidden Markov Model.
 *
 * This component is the UI orchestrator only. All probability work is delegated
 * to the pure modules in `src/lib/hmm` (`forward`, `viterbi`, `validateModel`,
 * `symbolsToIndices`). It owns editable model state, validates input at the
 * boundary, and renders results.
 */

import { useMemo, useState } from 'react';
import { forward } from '../../lib/hmm/forward';
import { viterbi } from '../../lib/hmm/viterbi';
import {
  type HMMModel,
  type ForwardResult,
  type ViterbiResult,
  validateModel,
  terminationWeights,
  symbolsToIndices,
} from '../../lib/hmm/types';
import MatrixEditor from './MatrixEditor';
import TrellisTable from './TrellisTable';

/** The course Lab 8 "ice-cream" preset (matches the test fixtures). */
function iceCreamModel(): HMMModel {
  return {
    states: ['hot', 'cold'],
    symbols: ['1', '2', '3'],
    start: [0.8, 0.2],
    end: [0.2, 0.2],
    A: [
      [0.2, 0.6],
      [0.3, 0.5],
    ],
    B: [
      [0.1, 0.15, 0.75],
      [0.8, 0.1, 0.1],
    ],
  };
}

const ICE_CREAM_SEQUENCE = '3 1 3';

interface RunResult {
  kind: 'forward' | 'viterbi';
  observedSymbols: string[];
  forward?: ForwardResult;
  viterbi?: ViterbiResult;
}

/** Parse a whitespace/comma separated observation string into symbol tokens. */
function parseSequence(raw: string): string[] {
  return raw
    .split(/[\s,]+/)
    .map((token) => token.trim())
    .filter((token) => token.length > 0);
}

/** Rebuild a matrix to new dimensions, preserving overlapping cells. */
function resizeMatrix(
  matrix: number[][],
  rows: number,
  cols: number,
  fill: number,
): number[][] {
  return Array.from({ length: rows }, (_, r) =>
    Array.from({ length: cols }, (_, c) => matrix[r]?.[c] ?? fill),
  );
}

/** Resize a vector, preserving overlapping entries. */
function resizeVector(vector: number[], length: number, fill: number): number[] {
  return Array.from({ length }, (_, i) => vector[i] ?? fill);
}

export default function Hmm() {
  const [model, setModel] = useState<HMMModel>(iceCreamModel);
  const [useEnd, setUseEnd] = useState(true);
  const [sequence, setSequence] = useState(ICE_CREAM_SEQUENCE);
  const [result, setResult] = useState<RunResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const effectiveModel = useMemo<HMMModel>(
    () => (useEnd ? model : { ...model, end: undefined }),
    [model, useEnd],
  );

  const problems = useMemo(
    () => validateModel(effectiveModel),
    [effectiveModel],
  );

  const observedTokens = useMemo(() => parseSequence(sequence), [sequence]);

  // --- state / symbol list editing -------------------------------------------

  function setStateName(index: number, name: string) {
    setModel((m) => ({
      ...m,
      states: m.states.map((s, i) => (i === index ? name : s)),
    }));
  }

  function addState() {
    setModel((m) => {
      const n = m.states.length + 1;
      return {
        ...m,
        states: [...m.states, `s${n}`],
        start: resizeVector(m.start, n, 0),
        end: m.end ? resizeVector(m.end, n, 1) : undefined,
        A: resizeMatrix(m.A, n, n, 0),
        B: resizeMatrix(m.B, n, m.symbols.length, 0),
      };
    });
    setResult(null);
  }

  function removeState(index: number) {
    setModel((m) => {
      if (m.states.length <= 1) return m;
      const keep = (_: unknown, i: number) => i !== index;
      return {
        ...m,
        states: m.states.filter(keep),
        start: m.start.filter(keep),
        end: m.end ? m.end.filter(keep) : undefined,
        A: m.A.filter(keep).map((row) => row.filter(keep)),
        B: m.B.filter(keep),
      };
    });
    setResult(null);
  }

  function setSymbolName(index: number, name: string) {
    setModel((m) => ({
      ...m,
      symbols: m.symbols.map((s, i) => (i === index ? name : s)),
    }));
  }

  function addSymbol() {
    setModel((m) => {
      const k = m.symbols.length + 1;
      return {
        ...m,
        symbols: [...m.symbols, `${k}`],
        B: resizeMatrix(m.B, m.states.length, k, 0),
      };
    });
    setResult(null);
  }

  function removeSymbol(index: number) {
    setModel((m) => {
      if (m.symbols.length <= 1) return m;
      const keep = (_: unknown, i: number) => i !== index;
      return {
        ...m,
        symbols: m.symbols.filter(keep),
        B: m.B.map((row) => row.filter(keep)),
      };
    });
    setResult(null);
  }

  // --- run / reset -----------------------------------------------------------

  function run(kind: 'forward' | 'viterbi') {
    setError(null);
    if (problems.length > 0) {
      setError('Fix the highlighted model problems before running.');
      setResult(null);
      return;
    }
    if (observedTokens.length === 0) {
      setError('Enter an observation sequence.');
      setResult(null);
      return;
    }
    try {
      const obs = symbolsToIndices(effectiveModel, observedTokens);
      if (kind === 'forward') {
        setResult({
          kind,
          observedSymbols: observedTokens,
          forward: forward(effectiveModel, obs),
        });
      } else {
        setResult({
          kind,
          observedSymbols: observedTokens,
          viterbi: viterbi(effectiveModel, obs),
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
      setResult(null);
    }
  }

  function loadIceCream() {
    setModel(iceCreamModel());
    setUseEnd(true);
    setSequence(ICE_CREAM_SEQUENCE);
    setResult(null);
    setError(null);
  }

  function clearAll() {
    setModel({
      states: ['s1', 's2'],
      symbols: ['a', 'b'],
      start: [0.5, 0.5],
      end: [1, 1],
      A: [
        [0.5, 0.5],
        [0.5, 0.5],
      ],
      B: [
        [0.5, 0.5],
        [0.5, 0.5],
      ],
    });
    setUseEnd(false);
    setSequence('');
    setResult(null);
    setError(null);
  }

  const ends = terminationWeights(effectiveModel);

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-6 p-4 sm:p-6">
      <header className="flex flex-col gap-1">
        <h2 className="text-lg font-semibold text-ink">Hidden Markov Model</h2>
        <p className="text-sm text-ink-muted">
          Forward likelihood <span className="font-mono">P(O)</span> and the
          Viterbi most-likely state path, with full trellis tables.
        </p>
      </header>

      <div className="flex flex-wrap gap-2">
        <ToolbarButton onClick={() => run('forward')}>Run Forward</ToolbarButton>
        <ToolbarButton onClick={() => run('viterbi')}>Run Viterbi</ToolbarButton>
        <ToolbarButton onClick={loadIceCream} variant="ghost">
          Load Lab 8 ice-cream example
        </ToolbarButton>
        <ToolbarButton onClick={clearAll} variant="ghost">
          Clear
        </ToolbarButton>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* States */}
        <Panel title="Hidden states">
          <ul className="flex flex-col gap-2">
            {model.states.map((state, i) => (
              <li key={i} className="flex items-center gap-2">
                <input
                  value={state}
                  onChange={(e) => setStateName(i, e.target.value)}
                  aria-label={`Hidden state ${i + 1} name`}
                  className="flex-1 rounded-md border border-border bg-surface-raised px-2 py-1.5 font-mono text-sm text-ink outline-none focus:ring-2 focus:ring-accent"
                />
                <button
                  type="button"
                  onClick={() => removeState(i)}
                  disabled={model.states.length <= 1}
                  aria-label={`Remove state ${state}`}
                  className="rounded-md border border-border px-2 py-1.5 text-xs text-ink-muted transition-colors hover:text-red-300 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
          <button
            type="button"
            onClick={addState}
            className="mt-2 rounded-md border border-border px-3 py-1.5 text-xs font-medium text-accent transition-colors hover:bg-surface-raised"
          >
            + Add state
          </button>
        </Panel>

        {/* Symbols */}
        <Panel title="Observation symbols">
          <ul className="flex flex-col gap-2">
            {model.symbols.map((symbol, i) => (
              <li key={i} className="flex items-center gap-2">
                <input
                  value={symbol}
                  onChange={(e) => setSymbolName(i, e.target.value)}
                  aria-label={`Observation symbol ${i + 1} name`}
                  className="flex-1 rounded-md border border-border bg-surface-raised px-2 py-1.5 font-mono text-sm text-ink outline-none focus:ring-2 focus:ring-accent"
                />
                <button
                  type="button"
                  onClick={() => removeSymbol(i)}
                  disabled={model.symbols.length <= 1}
                  aria-label={`Remove symbol ${symbol}`}
                  className="rounded-md border border-border px-2 py-1.5 text-xs text-ink-muted transition-colors hover:text-red-300 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
          <button
            type="button"
            onClick={addSymbol}
            className="mt-2 rounded-md border border-border px-3 py-1.5 text-xs font-medium text-accent transition-colors hover:bg-surface-raised"
          >
            + Add symbol
          </button>
        </Panel>
      </div>

      {/* Start / end vectors as single-row matrices */}
      <div className="grid gap-6 lg:grid-cols-2">
        <Panel title="Start probabilities (π)">
          <MatrixEditor
            caption="Initial-state distribution π"
            cornerLabel="π"
            rowLabels={['π']}
            colLabels={model.states}
            values={[model.start]}
            onChange={(next) =>
              setModel((m) => ({ ...m, start: next[0] ?? m.start }))
            }
            rowSumTarget={1}
          />
        </Panel>

        <Panel title="End probabilities">
          <label className="mb-3 flex items-center gap-2 text-sm text-ink">
            <input
              type="checkbox"
              checked={useEnd}
              onChange={(e) => {
                setUseEnd(e.target.checked);
                setResult(null);
              }}
              className="h-4 w-4 accent-accent"
            />
            Use explicit end (termination) probabilities
          </label>
          {useEnd ? (
            <MatrixEditor
              caption="Per-state termination weight"
              cornerLabel="end"
              rowLabels={['end']}
              colLabels={model.states}
              values={[model.end ?? model.states.map(() => 1)]}
              onChange={(next) =>
                setModel((m) => ({ ...m, end: next[0] ?? m.end }))
              }
            />
          ) : (
            <p className="text-sm text-ink-muted">
              Termination weight treated as 1 for every state (textbook Forward
              without an explicit final state).
            </p>
          )}
        </Panel>
      </div>

      {/* Transition and emission matrices */}
      <div className="grid gap-6 lg:grid-cols-2">
        <Panel title="Transition matrix A (from → to)">
          <MatrixEditor
            caption="A[from][to] — probability of moving from a state to another"
            cornerLabel="from \ to"
            rowLabels={model.states}
            colLabels={model.states}
            values={model.A}
            onChange={(next) => setModel((m) => ({ ...m, A: next }))}
            rowSumTarget={1}
            extraRowWeight={useEnd ? ends : undefined}
          />
        </Panel>

        <Panel title="Emission matrix B (state → symbol)">
          <MatrixEditor
            caption="B[state][symbol] — probability of emitting a symbol in a state"
            cornerLabel="state \ obs"
            rowLabels={model.states}
            colLabels={model.symbols}
            values={model.B}
            onChange={(next) => setModel((m) => ({ ...m, B: next }))}
            rowSumTarget={1}
          />
        </Panel>
      </div>

      {/* Observation sequence */}
      <Panel title="Observation sequence">
        <label
          htmlFor="hmm-sequence"
          className="mb-1 block text-xs text-ink-muted"
        >
          Symbols separated by spaces or commas (e.g. “{model.symbols.join(' ')}”).
        </label>
        <input
          id="hmm-sequence"
          value={sequence}
          onChange={(e) => setSequence(e.target.value)}
          placeholder={model.symbols.slice(0, 3).join(' ')}
          className="w-full rounded-md border border-border bg-surface-raised px-3 py-2 font-mono text-sm text-ink outline-none focus:ring-2 focus:ring-accent"
        />
        {observedTokens.length > 0 && (
          <p className="mt-1 text-xs text-ink-muted">
            {observedTokens.length} observation
            {observedTokens.length === 1 ? '' : 's'}:{' '}
            <span className="font-mono text-ink">{observedTokens.join(' ')}</span>
          </p>
        )}
      </Panel>

      {/* Validation / error messaging */}
      {problems.length > 0 && (
        <div
          role="alert"
          className="rounded-lg border border-amber-500/40 bg-amber-500/10 px-4 py-3 text-sm text-amber-200"
        >
          <p className="font-semibold">Model needs attention:</p>
          <ul className="mt-1 list-inside list-disc space-y-0.5">
            {problems.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </div>
      )}
      {error && (
        <div
          role="alert"
          className="rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200"
        >
          {error}
        </div>
      )}

      {/* Results */}
      {result?.kind === 'forward' && result.forward && (
        <section className="flex flex-col gap-4 rounded-xl border border-border bg-surface p-4">
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h3 className="text-sm font-semibold text-ink">Forward result</h3>
            <p className="font-mono text-sm text-ink-muted">
              P(O) ={' '}
              <span className="rounded bg-accent/20 px-2 py-0.5 font-semibold text-accent">
                {result.forward.prob.toPrecision(7)}
              </span>
            </p>
          </div>
          <TrellisTable
            title="α (forward) trellis"
            states={model.states}
            observations={result.observedSymbols}
            matrix={result.forward.trellis}
          />
        </section>
      )}

      {result?.kind === 'viterbi' && result.viterbi && (
        <section className="flex flex-col gap-4 rounded-xl border border-border bg-surface p-4">
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h3 className="text-sm font-semibold text-ink">Viterbi result</h3>
            <p className="font-mono text-sm text-ink-muted">
              P(best path) ={' '}
              <span className="rounded bg-accent/20 px-2 py-0.5 font-semibold text-accent">
                {result.viterbi.prob.toPrecision(7)}
              </span>
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="text-ink-muted">Best path:</span>
            {result.viterbi.path.map((state, i) => (
              <span key={i} className="flex items-center gap-2">
                <span className="rounded-md bg-accent/15 px-2 py-1 font-mono font-semibold text-accent">
                  {state}
                </span>
                {i < result.viterbi!.path.length - 1 && (
                  <span aria-hidden="true" className="text-ink-muted">
                    →
                  </span>
                )}
              </span>
            ))}
          </div>

          <TrellisTable
            title="δ (Viterbi) trellis — best path highlighted"
            states={model.states}
            observations={result.observedSymbols}
            matrix={result.viterbi.delta}
            pathIndices={result.viterbi.path.map((s) =>
              model.states.indexOf(s),
            )}
          />

          <TrellisTable
            title="Backpointers (predecessor state index; t=1 has none)"
            states={model.states}
            observations={result.observedSymbols}
            matrix={result.viterbi.backpointers}
            precision={0}
          />
        </section>
      )}
    </div>
  );
}

// --- small presentational helpers --------------------------------------------

function Panel({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section className="flex flex-col rounded-xl border border-border bg-surface p-4">
      <h3 className="mb-3 text-sm font-semibold text-ink">{title}</h3>
      {children}
    </section>
  );
}

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
        'rounded-md px-3 py-2 text-sm font-medium transition-colors outline-none focus-visible:ring-2 focus-visible:ring-accent',
        variant === 'solid'
          ? 'bg-accent/15 text-accent hover:bg-accent/25'
          : 'border border-border text-ink-muted hover:bg-surface-raised hover:text-ink',
      ].join(' ')}
    >
      {children}
    </button>
  );
}
