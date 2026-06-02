import { useRef } from 'react';

export interface TabDescriptor {
  /** Stable identifier used for state and panel association. */
  id: string;
  /** Human-readable label shown in the tab bar. */
  label: string;
}

interface TabsProps {
  tabs: readonly TabDescriptor[];
  activeId: string;
  onChange: (id: string) => void;
}

/**
 * Accessible tab bar for the app shell. Owns no module logic — it only renders
 * the four tab buttons and reports selection changes upward. Later agents fill
 * the panels, never this component.
 */
export default function Tabs({ tabs, activeId, onChange }: TabsProps) {
  const buttonRefs = useRef<Array<HTMLButtonElement | null>>([]);

  function focusTab(index: number) {
    const count = tabs.length;
    const next = ((index % count) + count) % count;
    const tab = tabs[next];
    if (!tab) return;
    onChange(tab.id);
    buttonRefs.current[next]?.focus();
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLButtonElement>, index: number) {
    switch (event.key) {
      case 'ArrowRight':
      case 'ArrowDown':
        event.preventDefault();
        focusTab(index + 1);
        break;
      case 'ArrowLeft':
      case 'ArrowUp':
        event.preventDefault();
        focusTab(index - 1);
        break;
      case 'Home':
        event.preventDefault();
        focusTab(0);
        break;
      case 'End':
        event.preventDefault();
        focusTab(tabs.length - 1);
        break;
      default:
        break;
    }
  }

  return (
    <div
      role="tablist"
      aria-label="xCalculator modules"
      aria-orientation="horizontal"
      className="flex items-center gap-1 border-b border-border bg-surface px-3 pt-2"
    >
      {tabs.map((tab, index) => {
        const selected = tab.id === activeId;
        return (
          <button
            key={tab.id}
            ref={(el) => {
              buttonRefs.current[index] = el;
            }}
            role="tab"
            type="button"
            id={`tab-${tab.id}`}
            aria-selected={selected}
            aria-controls={`panel-${tab.id}`}
            tabIndex={selected ? 0 : -1}
            onClick={() => onChange(tab.id)}
            onKeyDown={(event) => handleKeyDown(event, index)}
            className={[
              'relative -mb-px rounded-t-md px-4 py-2.5 text-sm font-medium transition-colors outline-none',
              'focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-0',
              selected
                ? 'bg-surface-raised text-ink'
                : 'text-ink-muted hover:bg-surface-raised/60 hover:text-ink',
            ].join(' ')}
          >
            {tab.label}
            {selected && (
              <span
                aria-hidden="true"
                className="absolute inset-x-2 -bottom-px h-0.5 rounded-full bg-accent"
              />
            )}
          </button>
        );
      })}
    </div>
  );
}
