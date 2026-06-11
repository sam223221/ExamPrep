# DOCUMENT.md — `app/static/`

## What lives here

The frontend for the app: a zero-build, fully-offline vanilla HTML/CSS/JS site with
a two-mode shell (**Lookup** | **Quiz**). Served by FastAPI's `StaticFiles` mount
at `/`. No framework, no bundler, no external network calls.

## Files (implemented — Phase D)

| File         | Purpose                                                                                  |
|--------------|------------------------------------------------------------------------------------------|
| `index.html` | Shell: sticky header, `Lookup \| Quiz` mode toggle (ARIA tablist), `#lookup-view`, `#quiz-view`, slide lightbox modal. Semantic landmarks (`header`/`main`/`footer`), skip link. Inline data-URI SVG `<link rel="icon">` (amber field-manual mark) — fully offline, silences the first-load `/favicon.ico` 404. |
| `style.css`  | The design system (see "Design" below). Mobile-first, light + dark via `prefers-color-scheme`, reduced-motion safe. |
| `common.js`  | Shared `SM.*` namespace: `escapeHtml`, `getJSON` (structured errors), `el` DOM builder, `/api/lectures` loader (drives chips + quiz selects), mode-toggle controller with roving-tabindex keyboard support, label helpers. |
| `lookup.js`  | Debounced (~220 ms) search → `GET /search`; lecture + topic filter chips; result cards (lecture/topic badges, `deck · p.X` citation, sim score, sanitized guide HTML, optional slide thumbnail); slide lightbox with focus management. |
| `quiz.js`    | Setup form (lecture/topic/difficulty/count) → `GET /api/quiz`; one-question-at-a-time runner with radio options, progress, prev/next, A–D keyboard select; submit → `POST /api/quiz/check`; results scoreboard + per-question review (right/wrong, correct answer, explanation, citation); "Retry these" / "New set". |

## Load order

`index.html` loads `common.js` → `lookup.js` → `quiz.js`. `common.js` defines the
global `SM` namespace and fires `SM.onLecturesReady(...)`; the two mode scripts
register callbacks against it, so order matters (common first). Mode switches emit
a `sm:modechange` CustomEvent that `lookup.js` listens to (to refocus the search box).

## API contract consumed (architecture §5.5 — frozen)

- `GET /search?q=&k=&lecture=&topic=` → `{query, results:[{text,html,score,lecture_id,topic,title,source_pdf,page,img}]}`
- `GET /slide?file=&page=` → PNG (opened in the lightbox via the `img` URL the server supplies)
- `GET /api/lectures` → `[{lecture_id,lecture_num,title,topics:[...],counts:{by_difficulty}}]`
- `GET /api/quiz?lecture=&topic=&difficulty=&n=&seed=` → `{count, questions:[{id,lecture_id,topic,difficulty,stem,options:[{key,text}]}]}` (no answer/explanation)
- `POST /api/quiz/check` body `{answers:[{id,chosen}]}` → `{score,total,results:[{id,correct,answer,explanation,source}]}`

## Key decisions

- **Data-driven filters.** Lecture (`L01…L11`) and topic chips/selects are built from
  `/api/lectures`, so adding Lecture 8/12 later needs **no** frontend edit. Lectures are
  re-sorted numerically client-side as a defensive guard against the non-padded sort hazard.
- **One shell, two modes.** A top-level ARIA tablist toggle swaps `#lookup-view` /
  `#quiz-view` without a router. Roving tabindex + arrow/Home/End keys per the WAI-ARIA
  tabs pattern.
- **Server is the grading authority.** Answers/explanations never ship in the `/api/quiz`
  payload; the client only learns correctness after `POST /api/quiz/check`. Submit is
  disabled until every question is answered.
- **Ephemeral quizzes.** No persistence (localStorage/etc.) per architecture open-Q #4.
- **Wide tables scroll inside their card, never the page.** `.result-body` is the
  horizontal-scroll container (`overflow-x: auto` + `-webkit-overflow-scrolling: touch`)
  and `.result-body table` is capped at `max-width: 100%`. Wide markdown tables (the
  guides' 3-column "Term | Definition | Source" definitions tables) therefore scroll
  within the result card on narrow viewports (~375px) instead of forcing the whole page
  to scroll horizontally. The slide thumbnail lives outside `.result-body` (appended to
  `.result-card`), so it is unaffected; the quiz runner has no `.result-body` and is
  likewise untouched. Desktop/tablet rendering is unchanged (no table overflows the card).
- **Offline favicon.** Inline `data:image/svg+xml,...` icon in `index.html` — no network
  request, consistent with the fully-offline constraint.

## Security (architecture §9)

- All model-derived text (search `text`, quiz `stem`/`option.text`/`explanation`/`source`,
  topics, titles) is rendered via `textContent` / the `el(...)` builder — never interpolated
  into `innerHTML`.
- The **single** `innerHTML` use is `result-body ← r.html`, which the server produces
  through the `bleach` allowlist (§5.6 step 4 / §9). The client does not sanitize raw model
  text; it only renders HTML the server already cleaned. This boundary is documented inline
  in `lookup.js` and `common.js`.
- The slide lightbox `src` comes only from the server-supplied `img` URL (a `/slide`
  endpoint link); no user-controlled path reaches it.

## Accessibility

- Semantic landmarks, a skip link, visible focus rings (custom `--focus` ring, paper-aware).
- Mode toggle is a proper ARIA `tablist`/`tab`/`tabpanel` with roving tabindex + arrow keys.
- Quiz options are a labelled `radiogroup`; each question's stem is the group label and is
  focused on navigation for screen-reader context. A–D keys select options.
- Modal: `role="dialog"` + `aria-modal`, Escape to close, focus moved to the close button
  on open and restored to the trigger on close, a minimal focus trap, and body scroll lock.
- Score ring exposes a text alternative via `role="img"` + `aria-label`.
- Contrast targets WCAG AA in both light and dark palettes; `prefers-reduced-motion`
  collapses all animation/transition durations.

## Design

"Engineering field manual" identity — deliberately distinct from the sibling `cyper`
app and from generic AI aesthetics: warm paper/ink palette with a single burnt-amber
accent and a deep-teal "verified" hue; humanist **serif** display face (Iowan / Palatino /
Georgia stack) paired with a system sans for UI and a monospace for all technical metadata
(badges, citations, counts); a faint fixed blueprint grid background; an 8px spacing rhythm.
No Inter, no purple gradients, no three-card hero grid. Motion is transform/opacity only.

## How it connects

`main.py` mounts this directory at `/` (last, after the API routes). `lookup.js`
calls `/search` and uses `/slide` image URLs; `quiz.js` calls `/api/quiz` and
`/api/quiz/check`; `common.js` calls `/api/lectures`.
