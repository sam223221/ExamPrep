/**
 * TrellisTable — renders an HMM dynamic-programming table (states × timesteps).
 *
 * Used in two modes:
 *   - Forward: the α table, with the final P(O) highlighted.
 *   - Viterbi: the δ table plus a backpointer table, with the cells on the
 *     recovered best path highlighted and the path shown step by step.
 *
 * Holds no probability logic — it only displays values passed in from the lib.
 */

interface TrellisTableProps {
  /** Heading shown above the table (e.g. "α (forward) trellis"). */
  title: string;
  /** Hidden-state names (rows). */
  states: string[];
  /** Observation symbols actually observed, in time order (column subheaders). */
  observations: string[];
  /** The DP matrix, indexed `[stateIndex][t]`. */
  matrix: number[][];
  /**
   * Optional path as state indices per timestep. When provided, the matching
   * cell in each column is highlighted (used for the Viterbi best path).
   */
  pathIndices?: number[];
  /** Number formatting precision for cells. */
  precision?: number;
}

function formatCell(value: number, precision: number): string {
  if (!Number.isFinite(value)) return '—';
  if (value === 0) return '0';
  // Scientific notation for very small probabilities so columns stay readable.
  if (value !== 0 && Math.abs(value) < 1e-4) return value.toExponential(2);
  return value.toFixed(precision);
}

export default function TrellisTable({
  title,
  states,
  observations,
  matrix,
  pathIndices,
  precision = 6,
}: TrellisTableProps) {
  const steps = observations.length;

  return (
    <div className="overflow-x-auto">
      <h4 className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink-muted">
        {title}
      </h4>
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr>
            <th
              scope="col"
              rowSpan={2}
              className="border border-border bg-surface px-2 py-1.5 text-left text-xs font-medium text-ink-muted align-bottom"
            >
              State
            </th>
            {Array.from({ length: steps }, (_, t) => (
              <th
                key={t}
                scope="col"
                className="border border-border bg-surface px-2 py-1 text-center text-xs font-medium text-ink-muted"
              >
                t={t + 1}
              </th>
            ))}
          </tr>
          <tr>
            {observations.map((symbol, t) => (
              <th
                key={t}
                scope="col"
                className="border border-border bg-surface px-2 py-1 text-center text-xs font-mono text-accent"
              >
                o={symbol}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {states.map((state, s) => (
            <tr key={s}>
              <th
                scope="row"
                className="border border-border bg-surface px-2 py-1.5 text-left text-xs font-semibold text-ink"
              >
                {state}
              </th>
              {Array.from({ length: steps }, (_, t) => {
                const onPath = pathIndices?.[t] === s;
                return (
                  <td
                    key={t}
                    aria-current={onPath ? 'true' : undefined}
                    className={[
                      'border border-border px-2 py-1.5 text-center font-mono text-xs tabular-nums',
                      onPath
                        ? 'bg-accent/20 font-semibold text-accent'
                        : 'text-ink',
                    ].join(' ')}
                  >
                    {formatCell(matrix[s]?.[t] ?? 0, precision)}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
