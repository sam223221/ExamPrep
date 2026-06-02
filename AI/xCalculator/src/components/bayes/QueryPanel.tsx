/**
 * QueryPanel — choose a query variable and evidence, then show
 * `P(query | evidence)` over the query variable's states.
 *
 * Inference is delegated to `src/lib/bayes/inference`. This component only
 * builds the query, runs it live on every relevant change, and renders the
 * resulting distribution as a numeric table with simple bars. It shows a clear
 * message when the network is invalid (CPTs not summing to 1, or not a DAG).
 */

import { useMemo, useState, useEffect } from 'react';
import {
  enumerationAsk,
  validateCpts,
  isDag,
} from '../../lib/bayes/inference';
import {
  type Assignment,
  type BayesNetworkModel,
  type BNNode,
} from '../../lib/bayes/types';

interface QueryPanelProps {
  network: BayesNetworkModel;
}

const UNSET = '__unset__';

export default function QueryPanel({ network }: QueryPanelProps) {
  const nodes = network.nodes;

  const [queryVar, setQueryVar] = useState<string>(nodes[0]?.id ?? '');
  const [evidence, setEvidence] = useState<Record<string, string>>({});

  // Keep the query variable valid as nodes come and go.
  useEffect(() => {
    if (nodes.length === 0) {
      if (queryVar !== '') setQueryVar('');
      return;
    }
    if (!nodes.some((n) => n.id === queryVar)) {
      setQueryVar(nodes[0]!.id);
    }
  }, [nodes, queryVar]);

  // Drop evidence entries for nodes/states that no longer exist.
  useEffect(() => {
    setEvidence((prev) => {
      const cleaned: Record<string, string> = {};
      let changed = false;
      for (const [id, value] of Object.entries(prev)) {
        const node = nodes.find((n) => n.id === id);
        if (node && node.states.includes(value)) {
          cleaned[id] = value;
        } else {
          changed = true;
        }
      }
      return changed ? cleaned : prev;
    });
  }, [nodes]);

  const cptProblems = useMemo(() => validateCpts(network), [network]);
  const dag = useMemo(() => isDag(network), [network]);

  const result = useMemo<{
    distribution?: Record<string, number>;
    error?: string;
  }>(() => {
    if (nodes.length === 0) return { error: 'Add a node to query the network.' };
    if (!dag) return { error: 'Network is not a DAG — remove the cycle to query.' };
    if (cptProblems.length > 0) {
      return { error: 'Fix the CPT problems below before querying.' };
    }
    const query = nodes.find((n) => n.id === queryVar);
    if (!query) return {};

    // Build evidence excluding the query variable and unset values.
    const cleanEvidence: Assignment = {};
    for (const [id, value] of Object.entries(evidence)) {
      if (id !== queryVar && value !== UNSET) cleanEvidence[id] = value;
    }

    try {
      return { distribution: enumerationAsk(queryVar, cleanEvidence, network) };
    } catch (err) {
      return { error: err instanceof Error ? err.message : String(err) };
    }
  }, [nodes, dag, cptProblems, queryVar, evidence, network]);

  const queryNode: BNNode | undefined = nodes.find((n) => n.id === queryVar);

  return (
    <aside className="flex w-full flex-col gap-4 overflow-y-auto border-l border-border bg-surface p-4">
      <h3 className="text-sm font-semibold text-ink">Query</h3>

      {nodes.length === 0 ? (
        <p className="text-sm text-ink-muted">
          Add nodes and connect them to run inference.
        </p>
      ) : (
        <>
          <label className="flex flex-col gap-1 text-xs text-ink-muted">
            Query variable
            <select
              value={queryVar}
              onChange={(e) => setQueryVar(e.target.value)}
              className="rounded-md border border-border bg-surface-raised px-2 py-1.5 text-sm text-ink outline-none focus:ring-2 focus:ring-accent"
            >
              {nodes.map((node) => (
                <option key={node.id} value={node.id}>
                  {node.name}
                </option>
              ))}
            </select>
          </label>

          <fieldset className="flex flex-col gap-2">
            <legend className="mb-1 text-xs font-medium uppercase tracking-wide text-ink-muted">
              Evidence
            </legend>
            {nodes
              .filter((node) => node.id !== queryVar)
              .map((node) => (
                <label
                  key={node.id}
                  className="flex items-center justify-between gap-2 text-sm text-ink"
                >
                  <span className="truncate">{node.name}</span>
                  <select
                    value={evidence[node.id] ?? UNSET}
                    onChange={(e) =>
                      setEvidence((prev) => ({
                        ...prev,
                        [node.id]: e.target.value,
                      }))
                    }
                    aria-label={`Evidence for ${node.name}`}
                    className="rounded-md border border-border bg-surface-raised px-2 py-1 text-sm text-ink outline-none focus:ring-2 focus:ring-accent"
                  >
                    <option value={UNSET}>unset</option>
                    {node.states.map((state) => (
                      <option key={state} value={state}>
                        {state}
                      </option>
                    ))}
                  </select>
                </label>
              ))}
            {nodes.length === 1 && (
              <p className="text-xs text-ink-muted">
                No other variables to set as evidence.
              </p>
            )}
          </fieldset>

          <div className="rounded-lg border border-border bg-surface-raised p-3">
            <h4 className="mb-2 text-xs font-medium uppercase tracking-wide text-ink-muted">
              {queryNode ? `P(${queryNode.name} | evidence)` : 'Result'}
            </h4>
            {result.error ? (
              <p role="alert" className="text-sm text-amber-300">
                {result.error}
              </p>
            ) : result.distribution && queryNode ? (
              <ul className="flex flex-col gap-2">
                {queryNode.states.map((state) => {
                  const p = result.distribution![state] ?? 0;
                  return (
                    <li key={state} className="flex flex-col gap-1">
                      <div className="flex items-baseline justify-between text-sm">
                        <span className="font-mono text-ink">{state}</span>
                        <span className="font-mono tabular-nums text-accent">
                          {p.toFixed(6)}
                        </span>
                      </div>
                      <div
                        className="h-2 overflow-hidden rounded-full bg-base"
                        role="img"
                        aria-label={`${state}: ${(p * 100).toFixed(2)} percent`}
                      >
                        <div
                          className="h-full rounded-full bg-accent transition-[width] duration-200"
                          style={{ width: `${Math.max(0, Math.min(100, p * 100))}%` }}
                        />
                      </div>
                    </li>
                  );
                })}
              </ul>
            ) : (
              <p className="text-sm text-ink-muted">No result.</p>
            )}
          </div>

          {cptProblems.length > 0 && (
            <div
              role="alert"
              className="rounded-lg border border-amber-500/40 bg-amber-500/10 px-3 py-2 text-xs text-amber-200"
            >
              <p className="font-semibold">CPT problems:</p>
              <ul className="mt-1 list-inside list-disc space-y-0.5">
                {cptProblems.map((p, i) => (
                  <li key={i}>{p}</li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </aside>
  );
}
