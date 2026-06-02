import { useCallback, useEffect, useRef, useState } from 'react';
import { evaluate, CalcError } from '../../lib/calc';

/** A completed calculation kept in the session history list. */
interface HistoryEntry {
  id: number;
  expression: string;
  result: string;
}

/** Logical role of a calculator key, used to drive styling. */
type KeyKind = 'digit' | 'operator' | 'function' | 'equals';

interface KeyDef {
  /** Glyph shown on the button. */
  label: string;
  /** Text appended to the expression (omitted for action keys). */
  insert?: string;
  /** Action keys instead of plain inserts. */
  action?: 'equals' | 'clear' | 'backspace' | 'negate' | 'percent';
  kind: KeyKind;
  /** Accessible name when the glyph alone is ambiguous. */
  ariaLabel?: string;
}

// 5-column grid layout. Order matters: it maps row-by-row onto the CSS grid.
const KEYS: KeyDef[] = [
  { label: 'C', action: 'clear', kind: 'function', ariaLabel: 'Clear' },
  { label: '(', insert: '(', kind: 'function', ariaLabel: 'Open parenthesis' },
  { label: ')', insert: ')', kind: 'function', ariaLabel: 'Close parenthesis' },
  { label: '^', insert: '^', kind: 'operator', ariaLabel: 'Power' },
  { label: '⌫', action: 'backspace', kind: 'function', ariaLabel: 'Backspace' },

  { label: '7', insert: '7', kind: 'digit' },
  { label: '8', insert: '8', kind: 'digit' },
  { label: '9', insert: '9', kind: 'digit' },
  { label: '÷', insert: '/', kind: 'operator', ariaLabel: 'Divide' },
  { label: '%', action: 'percent', kind: 'function', ariaLabel: 'Percent' },

  { label: '4', insert: '4', kind: 'digit' },
  { label: '5', insert: '5', kind: 'digit' },
  { label: '6', insert: '6', kind: 'digit' },
  { label: '×', insert: '*', kind: 'operator', ariaLabel: 'Multiply' },
  { label: '±', action: 'negate', kind: 'function', ariaLabel: 'Toggle sign' },

  { label: '1', insert: '1', kind: 'digit' },
  { label: '2', insert: '2', kind: 'digit' },
  { label: '3', insert: '3', kind: 'digit' },
  { label: '−', insert: '-', kind: 'operator', ariaLabel: 'Subtract' },
  { label: '+', insert: '+', kind: 'operator', ariaLabel: 'Add' },

  { label: '0', insert: '0', kind: 'digit' },
  { label: '.', insert: '.', kind: 'digit', ariaLabel: 'Decimal point' },
  { label: '=', action: 'equals', kind: 'equals', ariaLabel: 'Equals' },
];

/**
 * True when `expr` is a single balanced `-( … )` group, i.e. it starts with
 * `-(` and the parenthesis opened at index 1 is closed by the very last
 * character. Used by `negate()` to decide whether toggling the sign can simply
 * strip the wrapper. For `-(1)+(2)` the leading `(` closes at the `)` after `1`,
 * not at the end, so this returns false and the expression is re-wrapped instead.
 */
function isFullyNegatedGroup(expr: string): boolean {
  if (!expr.startsWith('-(') || !expr.endsWith(')')) return false;
  // Walk from the opening paren at index 1; the group is "full" only if depth
  // first returns to zero exactly at the final character.
  let depth = 0;
  for (let i = 1; i < expr.length; i += 1) {
    const ch = expr[i];
    if (ch === '(') depth += 1;
    else if (ch === ')') {
      depth -= 1;
      if (depth === 0) return i === expr.length - 1;
    }
  }
  return false;
}

/** Format a numeric result for display, trimming float noise without losing precision. */
function formatResult(value: number): string {
  if (Number.isInteger(value)) return String(value);
  // Round long mantissas to 12 significant digits, then drop trailing zeros.
  const rounded = Number.parseFloat(value.toPrecision(12));
  return String(rounded);
}

const KIND_CLASSES: Record<KeyKind, string> = {
  digit: 'bg-surface-raised text-ink hover:bg-surface-raised/70',
  operator: 'bg-surface-raised text-accent hover:bg-surface-raised/70',
  function: 'bg-surface text-ink-muted hover:bg-surface-raised/60 hover:text-ink',
  equals: 'bg-accent text-base font-semibold hover:bg-accent-strong',
};

let nextHistoryId = 0;

/**
 * Button-grid arithmetic calculator. Maintains the live expression string and a
 * result display; `=` / Enter evaluate via the safe shunting-yard parser in
 * `lib/calc.ts`. Errors surface as a friendly inline message rather than a crash.
 * Full keyboard input mirrors the buttons. A session history of `expr = result`
 * is kept in component state (no persistence); clicking an entry reloads it.
 */
export default function Calculator() {
  const [expression, setExpression] = useState('');
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const rootRef = useRef<HTMLDivElement>(null);

  const append = useCallback((text: string) => {
    setError(null);
    setResult(null);
    setExpression((prev) => prev + text);
  }, []);

  const clearAll = useCallback(() => {
    setExpression('');
    setResult(null);
    setError(null);
  }, []);

  const backspace = useCallback(() => {
    setError(null);
    setResult(null);
    setExpression((prev) => prev.slice(0, -1));
  }, []);

  /** Wrap the whole current expression in unary minus, or unwrap it if already negated. */
  const negate = useCallback(() => {
    setError(null);
    setResult(null);
    setExpression((prev) => {
      const trimmed = prev.trim();
      if (trimmed === '') return prev;
      // Only unwrap a leading `-(…)` when it is a single balanced group spanning
      // the whole expression — i.e. the `(` at index 1 matches the final `)`.
      // Without this check, `-(1)+(2)` would mis-unwrap to `1)+(2`.
      if (isFullyNegatedGroup(trimmed)) {
        return trimmed.slice(2, -1);
      }
      return `-(${trimmed})`;
    });
  }, []);

  /** Treat `%` as "divide the current expression by 100". */
  const percent = useCallback(() => {
    setError(null);
    setResult(null);
    setExpression((prev) => {
      const trimmed = prev.trim();
      if (trimmed === '') return prev;
      return `(${trimmed})/100`;
    });
  }, []);

  const compute = useCallback(() => {
    const trimmed = expression.trim();
    if (trimmed === '') return;
    try {
      const value = evaluate(trimmed);
      const formatted = formatResult(value);
      setResult(formatted);
      setError(null);
      setHistory((prev) => [
        { id: nextHistoryId++, expression: trimmed, result: formatted },
        ...prev,
      ]);
    } catch (err) {
      const message = err instanceof CalcError ? err.message : 'Could not evaluate expression';
      setError(message);
      setResult(null);
    }
  }, [expression]);

  const reloadEntry = useCallback((entry: HistoryEntry) => {
    setExpression(entry.expression);
    setResult(entry.result);
    setError(null);
    rootRef.current?.focus();
  }, []);

  const clearHistory = useCallback(() => setHistory([]), []);

  // Global-ish keyboard support scoped to the calculator panel via a focusable root.
  const handleKeyDown = useCallback(
    (event: React.KeyboardEvent<HTMLDivElement>) => {
      const { key } = event;

      if (key === 'Enter' || key === '=') {
        event.preventDefault();
        compute();
        return;
      }
      if (key === 'Escape') {
        event.preventDefault();
        clearAll();
        return;
      }
      if (key === 'Backspace') {
        event.preventDefault();
        backspace();
        return;
      }
      if (key === '%') {
        event.preventDefault();
        percent();
        return;
      }
      // Digits, decimal point, parentheses, and the binary operators map straight through.
      if (/^[0-9.()+\-*/^]$/.test(key)) {
        event.preventDefault();
        append(key);
      }
    },
    [append, backspace, clearAll, compute, percent],
  );

  // Autofocus the panel so keyboard entry works immediately when the tab opens.
  useEffect(() => {
    rootRef.current?.focus();
  }, []);

  const displayExpression = expression === '' ? '0' : expression;

  return (
    <div
      ref={rootRef}
      role="application"
      aria-label="Arithmetic calculator"
      tabIndex={0}
      onKeyDown={handleKeyDown}
      className="mx-auto flex h-full max-w-5xl flex-col gap-6 p-4 outline-none focus-visible:ring-2 focus-visible:ring-accent sm:p-6"
    >
      <div className="grid flex-1 grid-cols-1 gap-6 lg:grid-cols-[minmax(0,1fr)_18rem]">
        {/* Calculator surface */}
        <section className="flex flex-col gap-4" aria-label="Calculator">
          <div className="rounded-xl border border-border bg-surface p-4 shadow-lg">
            <div
              className="min-h-7 break-all text-right font-mono text-sm text-ink-muted"
              aria-hidden="true"
            >
              {displayExpression}
            </div>
            <output
              aria-live="polite"
              className="mt-1 block break-all text-right font-mono text-3xl font-semibold tracking-tight text-ink"
            >
              {error ? (
                <span className="text-sm font-normal text-red-400" role="alert">
                  {error}
                </span>
              ) : (
                (result ?? displayExpression)
              )}
            </output>
          </div>

          <div className="grid grid-cols-5 gap-2">
            {KEYS.map((keyDef) => {
              const isWide = keyDef.action === 'equals';
              return (
                <button
                  key={keyDef.label}
                  type="button"
                  aria-label={keyDef.ariaLabel}
                  onClick={() => {
                    switch (keyDef.action) {
                      case 'equals':
                        compute();
                        break;
                      case 'clear':
                        clearAll();
                        break;
                      case 'backspace':
                        backspace();
                        break;
                      case 'negate':
                        negate();
                        break;
                      case 'percent':
                        percent();
                        break;
                      default:
                        if (keyDef.insert !== undefined) append(keyDef.insert);
                    }
                    rootRef.current?.focus();
                  }}
                  className={[
                    'h-14 rounded-lg text-lg font-medium transition-colors outline-none',
                    'focus-visible:ring-2 focus-visible:ring-accent',
                    'active:scale-[0.98] motion-reduce:active:scale-100',
                    KIND_CLASSES[keyDef.kind],
                    isWide ? 'col-span-3' : '',
                  ].join(' ')}
                >
                  {keyDef.label}
                </button>
              );
            })}
          </div>
        </section>

        {/* History */}
        <aside
          className="flex min-h-0 flex-col rounded-xl border border-border bg-surface"
          aria-label="Calculation history"
        >
          <div className="flex items-center justify-between border-b border-border px-4 py-3">
            <h2 className="text-sm font-semibold text-ink">History</h2>
            <button
              type="button"
              onClick={clearHistory}
              disabled={history.length === 0}
              className="rounded px-2 py-1 text-xs text-ink-muted transition-colors outline-none hover:text-ink focus-visible:ring-2 focus-visible:ring-accent disabled:cursor-not-allowed disabled:opacity-40"
            >
              Clear
            </button>
          </div>

          {history.length === 0 ? (
            <p className="px-4 py-6 text-center text-xs text-ink-muted">
              No calculations yet. Press <kbd className="font-mono">=</kbd> to record one.
            </p>
          ) : (
            <ul className="min-h-0 flex-1 divide-y divide-border overflow-auto">
              {history.map((entry) => (
                <li key={entry.id}>
                  <button
                    type="button"
                    onClick={() => reloadEntry(entry)}
                    className="block w-full px-4 py-2.5 text-right transition-colors outline-none hover:bg-surface-raised focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-accent"
                  >
                    <span className="block break-all font-mono text-xs text-ink-muted">
                      {entry.expression}
                    </span>
                    <span className="block break-all font-mono text-sm font-semibold text-ink">
                      = {entry.result}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </aside>
      </div>

      <p className="text-center text-xs text-ink-muted">
        Keyboard: type digits & operators, <kbd className="font-mono">Enter</kbd> evaluates,{' '}
        <kbd className="font-mono">Esc</kbd> clears, <kbd className="font-mono">Backspace</kbd>{' '}
        deletes.
      </p>
    </div>
  );
}
