/**
 * MatrixEditor — a reusable, accessible editable numeric grid.
 *
 * Renders a labelled matrix (row headers + column headers) of probability
 * inputs in [0, 1]. Optionally validates per-row sums and highlights rows that
 * do not sum to the expected target, showing the current sum. Holds no
 * probability logic of its own — it is a controlled component that reports edits
 * upward via `onChange`.
 */

interface MatrixEditorProps {
  /** Accessible caption / heading for this grid. */
  caption: string;
  /** Labels for each row (length = number of rows). */
  rowLabels: string[];
  /** Labels for each column (length = number of columns). */
  colLabels: string[];
  /** Current values, indexed `[row][col]`. */
  values: number[][];
  /** Called with the full updated matrix when a single cell changes. */
  onChange: (next: number[][]) => void;
  /**
   * When set, each row's sum is validated against this target (typically 1) and
   * off-target rows are highlighted with their current sum. Omit to disable.
   */
  rowSumTarget?: number;
  /**
   * Optional extra weight added to a row's sum before validation, indexed by
   * row. Used by the HMM transition matrix where each row competes with a
   * per-state "end" weight so that row + end = 1.
   */
  extraRowWeight?: number[];
  /** Tolerance for the row-sum check. */
  tolerance?: number;
  /** Short label describing what a row represents (used in the header cell). */
  cornerLabel?: string;
}

const NUMBER_FORMAT = (value: number) =>
  Number.isFinite(value) ? value.toFixed(4).replace(/\.?0+$/, '') : '0';

export default function MatrixEditor({
  caption,
  rowLabels,
  colLabels,
  values,
  onChange,
  rowSumTarget,
  extraRowWeight,
  tolerance = 1e-6,
  cornerLabel = '',
}: MatrixEditorProps) {
  function handleCellChange(row: number, col: number, raw: string) {
    const parsed = raw === '' ? 0 : Number(raw);
    const clamped = Number.isFinite(parsed)
      ? Math.min(1, Math.max(0, parsed))
      : 0;
    const next = values.map((r, ri) =>
      ri === row ? r.map((c, ci) => (ci === col ? clamped : c)) : [...r],
    );
    onChange(next);
  }

  function rowSum(row: number): number {
    const base = (values[row] ?? []).reduce((acc, v) => acc + v, 0);
    return base + (extraRowWeight?.[row] ?? 0);
  }

  const validate = rowSumTarget !== undefined;

  return (
    <figure className="m-0 overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <caption className="mb-2 text-left text-xs font-semibold uppercase tracking-wide text-ink-muted">
          {caption}
        </caption>
        <thead>
          <tr>
            <th
              scope="col"
              className="border border-border bg-surface px-2 py-1.5 text-left text-xs font-medium text-ink-muted"
            >
              {cornerLabel}
            </th>
            {colLabels.map((label, ci) => (
              <th
                key={ci}
                scope="col"
                className="border border-border bg-surface px-2 py-1.5 text-center text-xs font-semibold text-ink"
              >
                {label}
              </th>
            ))}
            {validate && (
              <th
                scope="col"
                className="border border-border bg-surface px-2 py-1.5 text-center text-xs font-medium text-ink-muted"
              >
                Σ
              </th>
            )}
          </tr>
        </thead>
        <tbody>
          {rowLabels.map((rowLabel, ri) => {
            const sum = rowSum(ri);
            const offTarget =
              validate && Math.abs(sum - rowSumTarget!) > tolerance;
            return (
              <tr key={ri}>
                <th
                  scope="row"
                  className="border border-border bg-surface px-2 py-1.5 text-left text-xs font-semibold text-ink"
                >
                  {rowLabel}
                </th>
                {colLabels.map((_, ci) => (
                  <td key={ci} className="border border-border p-0">
                    <input
                      type="number"
                      inputMode="decimal"
                      min={0}
                      max={1}
                      step={0.01}
                      value={NUMBER_FORMAT(values[ri]?.[ci] ?? 0)}
                      onChange={(e) => handleCellChange(ri, ci, e.target.value)}
                      aria-label={`${caption}: ${rowLabel} to ${colLabels[ci]}`}
                      className="w-full bg-surface-raised px-2 py-1.5 text-center font-mono text-ink outline-none focus:bg-base focus:ring-2 focus:ring-inset focus:ring-accent"
                    />
                  </td>
                ))}
                {validate && (
                  <td
                    className={[
                      'border border-border px-2 py-1.5 text-center font-mono text-xs tabular-nums',
                      offTarget
                        ? 'bg-red-500/15 font-semibold text-red-300'
                        : 'text-ink-muted',
                    ].join(' ')}
                  >
                    {sum.toFixed(3)}
                  </td>
                )}
              </tr>
            );
          })}
        </tbody>
      </table>
      {validate && (
        <figcaption className="mt-1 text-xs text-ink-muted">
          {extraRowWeight
            ? `Each row plus its end weight must sum to ${rowSumTarget}.`
            : `Each row must sum to ${rowSumTarget}.`}
        </figcaption>
      )}
    </figure>
  );
}
