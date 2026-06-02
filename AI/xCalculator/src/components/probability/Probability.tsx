import { useId, useMemo, useState } from 'react';
import {
  factorial,
  permutations,
  combinations,
  complement,
  unionProb,
  intersectionIndependent,
  conditional,
  bayes,
  ProbabilityError,
} from '../../lib/probability';

/**
 * Probability module. Three sections — Combinatorics, Probability rules, and
 * Bayes' theorem — each a labelled form that shows its formula and a live result.
 * All math lives in `lib/probability.ts`; this component only collects inputs,
 * calls the pure functions, and renders results or inline validation messages.
 * Invalid or out-of-range inputs surface a message and never crash.
 */
export default function Probability() {
  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-8 p-4 sm:p-6">
      <Combinatorics />
      <ProbabilityRules />
      <Bayes />
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Shared presentational pieces                                        */
/* ------------------------------------------------------------------ */

interface SectionProps {
  title: string;
  description: string;
  children: React.ReactNode;
}

function Section({ title, description, children }: SectionProps) {
  return (
    <section className="rounded-xl border border-border bg-surface p-5 shadow-lg">
      <header className="mb-4">
        <h2 className="text-[0.9375rem] font-semibold text-ink">{title}</h2>
        <p className="mt-0.5 text-xs text-ink-muted">{description}</p>
      </header>
      <div className="flex flex-col gap-5">{children}</div>
    </section>
  );
}

/** A monospace formula line. */
function Formula({ children }: { children: React.ReactNode }) {
  return (
    <p className="rounded-md bg-base/60 px-3 py-2 font-mono text-xs text-ink-muted">
      {children}
    </p>
  );
}

interface NumberFieldProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  /** `integer` for combinatorics (step 1), `probability` for [0,1] (step 0.01). */
  variant: 'integer' | 'probability';
}

function NumberField({ label, value, onChange, variant }: NumberFieldProps) {
  const id = useId();
  const isProb = variant === 'probability';
  return (
    <div className="flex flex-col gap-1">
      <label htmlFor={id} className="text-xs font-medium text-ink-muted">
        {label}
      </label>
      <input
        id={id}
        type="number"
        inputMode={isProb ? 'decimal' : 'numeric'}
        step={isProb ? 0.01 : 1}
        min={isProb ? 0 : 0}
        max={isProb ? 1 : undefined}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="w-full rounded-md border border-border bg-surface-raised px-3 py-2 font-mono text-sm text-ink outline-none transition-colors focus:border-accent focus-visible:ring-2 focus-visible:ring-accent"
      />
    </div>
  );
}

/** Result row: either a value or an inline error message tied to the section. */
function ResultLine({ label, error, value }: { label: string; error: string | null; value: string }) {
  return (
    <div
      className={[
        'flex items-baseline justify-between gap-3 rounded-md border px-3 py-2.5',
        error ? 'border-red-500/40 bg-red-500/10' : 'border-accent/30 bg-accent/10',
      ].join(' ')}
    >
      <span className="text-xs font-medium text-ink-muted">{label}</span>
      {error ? (
        <span role="alert" className="text-right text-sm text-red-300">
          {error}
        </span>
      ) : (
        <span className="font-mono text-lg font-semibold text-accent">{value}</span>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Parsing helpers                                                     */
/* ------------------------------------------------------------------ */

/** Parse a string into a finite number, or null if blank/invalid. */
function parseNum(raw: string): number | null {
  const trimmed = raw.trim();
  if (trimmed === '') return null;
  const n = Number(trimmed);
  return Number.isFinite(n) ? n : null;
}

/** Format a probability/number result with up to 6 significant digits, trimming zeros. */
function fmt(value: number): string {
  if (Number.isInteger(value)) return String(value);
  return String(Number.parseFloat(value.toPrecision(6)));
}

/**
 * Run a pure computation, mapping a thrown {@link ProbabilityError} (or blank
 * inputs) to an inline error string. Returns `{ value }` or `{ error }`.
 */
function safeCompute(fn: () => string, inputsReady: boolean): { value: string; error: string | null } {
  if (!inputsReady) return { value: '—', error: null };
  try {
    return { value: fn(), error: null };
  } catch (err) {
    const message =
      err instanceof ProbabilityError ? err.message : 'Invalid input';
    return { value: '—', error: message };
  }
}

/* ------------------------------------------------------------------ */
/* Section: Combinatorics                                              */
/* ------------------------------------------------------------------ */

function Combinatorics() {
  const [nFact, setNFact] = useState('6');
  const [nPerm, setNPerm] = useState('5');
  const [rPerm, setRPerm] = useState('2');
  const [nComb, setNComb] = useState('5');
  const [rComb, setRComb] = useState('2');

  const factResult = useMemo(() => {
    const n = parseNum(nFact);
    return safeCompute(() => fmt(factorial(n as number)), n !== null);
  }, [nFact]);

  const permResult = useMemo(() => {
    const n = parseNum(nPerm);
    const r = parseNum(rPerm);
    return safeCompute(() => fmt(permutations(n as number, r as number)), n !== null && r !== null);
  }, [nPerm, rPerm]);

  const combResult = useMemo(() => {
    const n = parseNum(nComb);
    const r = parseNum(rComb);
    return safeCompute(() => fmt(combinations(n as number, r as number)), n !== null && r !== null);
  }, [nComb, rComb]);

  return (
    <Section
      title="Combinatorics"
      description="Factorials, permutations, and combinations (exact integer arithmetic)."
    >
      {/* Factorial */}
      <div className="flex flex-col gap-2">
        <Formula>n! = n · (n−1) · … · 2 · 1</Formula>
        <div className="grid gap-3 sm:grid-cols-[8rem_1fr] sm:items-end">
          <NumberField label="n" value={nFact} onChange={setNFact} variant="integer" />
          <ResultLine label="n!" error={factResult.error} value={factResult.value} />
        </div>
      </div>

      {/* Permutations */}
      <div className="flex flex-col gap-2">
        <Formula>nPr = n! / (n − r)!</Formula>
        <div className="grid gap-3 sm:grid-cols-[1fr_1fr_1.4fr] sm:items-end">
          <NumberField label="n" value={nPerm} onChange={setNPerm} variant="integer" />
          <NumberField label="r" value={rPerm} onChange={setRPerm} variant="integer" />
          <ResultLine label="nPr" error={permResult.error} value={permResult.value} />
        </div>
      </div>

      {/* Combinations */}
      <div className="flex flex-col gap-2">
        <Formula>nCr = n! / (r! · (n − r)!)</Formula>
        <div className="grid gap-3 sm:grid-cols-[1fr_1fr_1.4fr] sm:items-end">
          <NumberField label="n" value={nComb} onChange={setNComb} variant="integer" />
          <NumberField label="r" value={rComb} onChange={setRComb} variant="integer" />
          <ResultLine label="nCr" error={combResult.error} value={combResult.value} />
        </div>
      </div>
    </Section>
  );
}

/* ------------------------------------------------------------------ */
/* Section: Probability rules                                          */
/* ------------------------------------------------------------------ */

function ProbabilityRules() {
  const [compP, setCompP] = useState('0.3');

  const [unionA, setUnionA] = useState('0.5');
  const [unionB, setUnionB] = useState('0.4');
  const [unionAB, setUnionAB] = useState('0.2');

  const [interA, setInterA] = useState('0.5');
  const [interB, setInterB] = useState('0.4');

  const [condAB, setCondAB] = useState('0.2');
  const [condB, setCondB] = useState('0.5');

  const compResult = useMemo(() => {
    const p = parseNum(compP);
    return safeCompute(() => fmt(complement(p as number)), p !== null);
  }, [compP]);

  const unionResult = useMemo(() => {
    const a = parseNum(unionA);
    const b = parseNum(unionB);
    const ab = parseNum(unionAB);
    return safeCompute(
      () => fmt(unionProb(a as number, b as number, ab as number)),
      a !== null && b !== null && ab !== null,
    );
  }, [unionA, unionB, unionAB]);

  const interResult = useMemo(() => {
    const a = parseNum(interA);
    const b = parseNum(interB);
    return safeCompute(
      () => fmt(intersectionIndependent(a as number, b as number)),
      a !== null && b !== null,
    );
  }, [interA, interB]);

  const condResult = useMemo(() => {
    const ab = parseNum(condAB);
    const b = parseNum(condB);
    return safeCompute(() => fmt(conditional(ab as number, b as number)), ab !== null && b !== null);
  }, [condAB, condB]);

  return (
    <Section
      title="Probability rules"
      description="Complement, union, intersection (independent), and conditional. Inputs are probabilities in [0, 1]."
    >
      {/* Complement */}
      <div className="flex flex-col gap-2">
        <Formula>P(¬A) = 1 − P(A)</Formula>
        <div className="grid gap-3 sm:grid-cols-[8rem_1fr] sm:items-end">
          <NumberField label="P(A)" value={compP} onChange={setCompP} variant="probability" />
          <ResultLine label="P(¬A)" error={compResult.error} value={compResult.value} />
        </div>
      </div>

      {/* Union */}
      <div className="flex flex-col gap-2">
        <Formula>P(A∪B) = P(A) + P(B) − P(A∩B)</Formula>
        <div className="grid gap-3 sm:grid-cols-3 sm:items-end">
          <NumberField label="P(A)" value={unionA} onChange={setUnionA} variant="probability" />
          <NumberField label="P(B)" value={unionB} onChange={setUnionB} variant="probability" />
          <NumberField label="P(A∩B)" value={unionAB} onChange={setUnionAB} variant="probability" />
        </div>
        <ResultLine label="P(A∪B)" error={unionResult.error} value={unionResult.value} />
      </div>

      {/* Intersection (independent) */}
      <div className="flex flex-col gap-2">
        <Formula>P(A∩B) = P(A) · P(B)　(A, B independent)</Formula>
        <div className="grid gap-3 sm:grid-cols-[1fr_1fr_1.4fr] sm:items-end">
          <NumberField label="P(A)" value={interA} onChange={setInterA} variant="probability" />
          <NumberField label="P(B)" value={interB} onChange={setInterB} variant="probability" />
          <ResultLine label="P(A∩B)" error={interResult.error} value={interResult.value} />
        </div>
      </div>

      {/* Conditional */}
      <div className="flex flex-col gap-2">
        <Formula>P(A|B) = P(A∩B) / P(B)</Formula>
        <div className="grid gap-3 sm:grid-cols-[1fr_1fr_1.4fr] sm:items-end">
          <NumberField label="P(A∩B)" value={condAB} onChange={setCondAB} variant="probability" />
          <NumberField label="P(B)" value={condB} onChange={setCondB} variant="probability" />
          <ResultLine label="P(A|B)" error={condResult.error} value={condResult.value} />
        </div>
      </div>
    </Section>
  );
}

/* ------------------------------------------------------------------ */
/* Section: Bayes' theorem                                             */
/* ------------------------------------------------------------------ */

function Bayes() {
  const [pA, setPA] = useState('0.01');
  const [pBgivenA, setPBgivenA] = useState('0.99');
  const [pBgivenNotA, setPBgivenNotA] = useState('0.05');

  const computed = useMemo(() => {
    const a = parseNum(pA);
    const ba = parseNum(pBgivenA);
    const bna = parseNum(pBgivenNotA);
    if (a === null || ba === null || bna === null) {
      return { error: null as string | null, result: null };
    }
    try {
      return { error: null, result: bayes(a, ba, bna) };
    } catch (err) {
      const message = err instanceof ProbabilityError ? err.message : 'Invalid input';
      return { error: message, result: null };
    }
  }, [pA, pBgivenA, pBgivenNotA]);

  const posterior = computed.result ? fmt(computed.result.posterior) : '—';

  return (
    <Section
      title="Bayes' theorem"
      description="Total-probability form. Enter the prior and the two likelihoods; the posterior and its worked terms are shown."
    >
      <Formula>
        P(A|B) = P(B|A)·P(A) / [ P(B|A)·P(A) + P(B|¬A)·P(¬A) ]
      </Formula>

      <div className="grid gap-3 sm:grid-cols-3">
        <NumberField label="P(A) — prior" value={pA} onChange={setPA} variant="probability" />
        <NumberField label="P(B|A)" value={pBgivenA} onChange={setPBgivenA} variant="probability" />
        <NumberField
          label="P(B|¬A)"
          value={pBgivenNotA}
          onChange={setPBgivenNotA}
          variant="probability"
        />
      </div>

      <ResultLine label="P(A|B) — posterior" error={computed.error} value={posterior} />

      {computed.result && !computed.error && (
        <dl className="grid grid-cols-2 gap-x-4 gap-y-1.5 rounded-md bg-base/60 px-3 py-2.5 font-mono text-xs text-ink-muted sm:grid-cols-3">
          <div>
            <dt className="inline">P(¬A)</dt>
            <dd className="inline text-ink"> = {fmt(computed.result.priorComplement)}</dd>
          </div>
          <div>
            <dt className="inline">Numerator</dt>
            <dd className="inline text-ink"> = {fmt(computed.result.numerator)}</dd>
          </div>
          <div>
            <dt className="inline">Denom = P(B)</dt>
            <dd className="inline text-ink"> = {fmt(computed.result.denominator)}</dd>
          </div>
        </dl>
      )}
    </Section>
  );
}
