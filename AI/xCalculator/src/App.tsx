import { useState } from 'react';
import Tabs, { type TabDescriptor } from './components/Tabs';
import Calculator from './components/calculator/Calculator';
import Probability from './components/probability/Probability';
import BayesNetwork from './components/bayes/BayesNetwork';
import Hmm from './components/hmm/Hmm';

const TABS = [
  { id: 'calculator', label: 'Calculator' },
  { id: 'probability', label: 'Probability' },
  { id: 'bayes', label: 'Bayesian Network' },
  { id: 'hmm', label: 'HMM' },
] as const satisfies readonly TabDescriptor[];

type TabId = (typeof TABS)[number]['id'];

const PANELS: Record<TabId, () => React.JSX.Element> = {
  calculator: Calculator,
  probability: Probability,
  bayes: BayesNetwork,
  hmm: Hmm,
};

/**
 * App shell: owns active-tab state and renders the tab bar plus the active
 * module panel. Feature agents replace only the inner module components
 * (Calculator / Probability / BayesNetwork / Hmm); this shell stays fixed.
 */
export default function App() {
  const [activeId, setActiveId] = useState<TabId>('calculator');
  const ActivePanel = PANELS[activeId];

  return (
    <div className="flex h-full flex-col bg-base text-ink">
      <header className="flex items-center gap-3 border-b border-border bg-surface px-4 py-3">
        <span className="grid h-8 w-8 place-items-center rounded-md bg-accent/15 font-mono text-base font-bold text-accent">
          x
        </span>
        <div className="leading-tight">
          <h1 className="text-sm font-semibold tracking-tight">xCalculator</h1>
          <p className="text-xs text-ink-muted">AI exam study toolkit</p>
        </div>
      </header>

      <Tabs tabs={TABS} activeId={activeId} onChange={(id) => setActiveId(id as TabId)} />

      <main
        role="tabpanel"
        id={`panel-${activeId}`}
        aria-labelledby={`tab-${activeId}`}
        tabIndex={0}
        className="min-h-0 flex-1 overflow-auto bg-base outline-none"
      >
        <ActivePanel />
      </main>
    </div>
  );
}
