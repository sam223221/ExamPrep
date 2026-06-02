# L02 — Introduction to Agents — Figure Catalogue

Source PDF: `AI/Lecture2-Introduction to Agents.pdf` (38 slides).
Extraction tool: PyMuPDF (`fitz` 1.24.9) via `py -3.12`.

Every entry below records the figure's filename, source slide, surrounding
slide text / caption, the agent's relevance verdict (USE / REWORK / SKIP),
and a one-to-two-sentence rationale. Whole-slide page-renders are tagged
`EXTRACTION_METHOD: page-render`.

Verdict counts: USE = 10, REWORK = 12, SKIP = 13. Total catalogued = 35
(some xrefs are duplicated by PowerPoint across consecutive slides — those
duplicates are recorded as separate SKIPs because we already use the
canonical copy). All 22 USE + REWORK figures are embedded in the chapter.

---

## fig01-xref9-slide1.png

- **Slide:** 1 — title slide "Introduction to Agents".
- **Caption / surrounding text:** none — decorative slide background.
- **Verdict:** SKIP.
- **Rationale:** A near-black rectangle used as the title-slide background;
  carries no information.

## fig02-xref15-slide2.png

- **Slide:** 2 — section title "Intelligent Agents".
- **Caption / surrounding text:** none — a still of the Pixar character
  WALL-E on a rocky landscape, used decoratively to introduce the topic.
- **Verdict:** SKIP.
- **Rationale:** Decorative section-divider image. No teaching content.

## fig03-xref25-slide4.png

- **Slide:** 4 — "Agents". Caption: *An agent is anything that can be
  viewed as perceiving its environment through sensors and acting upon
  that environment through actuators.*
- **Verdict:** USE.
- **Rationale:** **Canonical agent ↔ environment block diagram.** Shows the
  feedback loop: environment → percepts → agent (with "?" inside, i.e. the
  agent function) → actions → environment. This is the most-cited image in
  every undergraduate AI course and must appear in §3.1 (Agent definition).

## fig04-xref30-slide6.png

- **Slide:** 6 — "Terminologies" slide. Same agent ↔ environment image
  re-used to anchor the definitions of percept, percept sequence, agent
  function, agent program.
- **Verdict:** SKIP.
- **Rationale:** Identical to fig03 (same image data, PowerPoint re-used
  the picture). Embedding twice would be visual clutter.

## fig05-xref37-slide7.png

- **Slide:** 7 — "Example: Vacuum-cleaner world". Caption: *Percepts:
  Location and status, e.g., [A, Dirty]; Actions: Left, Right, Suck, NoOp.*
- **Verdict:** USE.
- **Rationale:** The two-cell vacuum world (rooms A and B, robot in A,
  dirt in both) — the running worked example for the entire lecture.
  Required in §3 and §5.

## fig06-xref40-slide8.png

- **Slide:** 8 — "A Simple Agent Function" with a "?" placeholder.
- **Verdict:** SKIP.
- **Rationale:** Duplicate of fig05 (same xref pattern, vacuum-world image
  re-used). The slide-9 percept-action table (fig07) is the figure with
  teaching value here.

## fig07-xref41-slide8.png

- **Slide:** 8/9 — caption: *Percept sequence → Action table.*
- **Verdict:** USE.
- **Rationale:** **The percept-sequence-to-action lookup table** that
  defines what an agent function *is*, mathematically. Essential for §3.2
  (Agent function). Lists rows like `[A, Clean] → Right`, `[A, Dirty] →
  Suck`, plus longer percept-sequences.

## fig08-xref44-slide9.png

- **Slide:** 9 — vacuum world drawn beside the percept-action table.
- **Verdict:** SKIP.
- **Rationale:** Duplicate of fig05.

## fig09-xref45-slide9.png

- **Slide:** 9 — second copy of the percept-action table next to the
  vacuum-world drawing.
- **Verdict:** SKIP.
- **Rationale:** Duplicate of fig07. We use fig07 (slide-8 instance) as
  the canonical version because it is rendered cleanly without the
  adjacent vacuum-world image overlap.

## fig10-xref50-slide11.png

- **Slide:** 11/12 — "Is this a rational agent?" example.
- **Verdict:** SKIP.
- **Rationale:** Duplicate of fig05.

## fig11-xref63-slide17.png

- **Slide:** 17 — "Fully observable vs. partially observable". A top-down
  RoboCup-style soccer field with multiple coloured player tokens — the
  "fully observable" / overhead-view illustration.
- **Verdict:** REWORK.
- **Rationale:** The image alone doesn't tell the story — meaning depends
  on the contrast with fig12 (which shows the robot's-eye view). Embedded
  side-by-side with fig12 and accompanied by a prose caption that names
  which one is the fully-observable view and which the partially-observable
  view.

## fig12-xref64-slide17.png

- **Slide:** 17 — Photograph of two humanoid Nao robots; the
  partially-observable counterpart to fig11.
- **Verdict:** REWORK.
- **Rationale:** Pairs with fig11 to teach fully-vs-partially observable.
  Photo alone isn't self-explanatory; needs caption.

## fig13-xref67-slide18.png

- **Slide:** 18 — "Deterministic vs. stochastic". Checkers board.
- **Verdict:** REWORK.
- **Rationale:** Checkers as the deterministic example. Pairs with
  backgammon (fig14).

## fig14-xref68-slide18.png

- **Slide:** 18 — backgammon board with dice.
- **Verdict:** REWORK.
- **Rationale:** Backgammon as the stochastic example (dice introduce
  randomness). Pairs with fig13.

## fig15-xref71-slide19.png

- **Slide:** 19 — "Episodic vs. sequential". Pac-Man maze.
- **Verdict:** REWORK.
- **Rationale:** Pac-Man = sequential. Pairs with the spam-filter image
  for episodic.

## fig16-xref72-slide19.png

- **Slide:** 19 — Spam-filter diagram: incoming mail → filter → inbox or
  trash.
- **Verdict:** REWORK.
- **Rationale:** Spam filter = episodic. The slide places these two side
  by side to drive the contrast home.

## fig17-xref76-slide20.png

- **Slide:** 20 — "Static vs. dynamic". Rubik's cube.
- **Verdict:** REWORK.
- **Rationale:** Rubik's cube = static (puzzle doesn't change while you
  think). Pairs with the dashcam view (fig18) for dynamic.

## fig18-xref77-slide20.png

- **Slide:** 20 — Self-driving-car dashboard / road view.
- **Verdict:** REWORK.
- **Rationale:** Driving environment = dynamic (the world moves while the
  agent deliberates).

## fig19-xref80-slide21.png

- **Slide:** 21 — "Discrete vs. continuous". Chess-playing robot arm.
- **Verdict:** REWORK.
- **Rationale:** Chess robot is shown as the *continuous-actuation* counter-
  example to the discrete chess board (fig20). Caption clarifies.

## fig20-xref81-slide21.png

- **Slide:** 21 — Chess board top-down with the algebraic-notation
  coordinates.
- **Verdict:** REWORK.
- **Rationale:** Discrete game states (64 squares, finite move set). Pairs
  with fig19.

## fig21-xref84-slide22.png

- **Slide:** 22 — "Single agent vs. multiagent". Isometric drawing of a
  crowd of people walking through a narrow gap.
- **Verdict:** REWORK.
- **Rationale:** Multi-agent example.

## fig22-xref85-slide22.png

- **Slide:** 22 — Mouse in a maze.
- **Verdict:** REWORK.
- **Rationale:** Single-agent example. Pairs with fig21.

## fig23-xref88-slide23.png

- **Slide:** 23 — Chess with a clock (small thumbnail used in the example
  table).
- **Verdict:** SKIP.
- **Rationale:** This thumbnail is subsumed by the whole-slide page-render
  `slide23-page-render.png` which gives the complete classification table
  (the only figure that makes pedagogical sense for this slide).

## fig24-xref89-slide23.png

- **Slide:** 23 — Scrabble thumbnail in the classification table.
- **Verdict:** SKIP. (Same reason as fig23.)

## fig25-xref90-slide23.png

- **Slide:** 23 — Yellow taxi thumbnail (autonomous-driving column).
- **Verdict:** SKIP. (Same reason as fig23.)

## fig26-xref91-slide23.png

- **Slide:** 23 — Word-jumble puzzle thumbnail.
- **Verdict:** SKIP. (Same reason as fig23.)

## slide23-page-render.png

- **EXTRACTION_METHOD:** page-render (dpi=180).
- **Slide:** 23 — full slide: *Examples of different environments.* A
  table with four columns (Word-jumble solver, Chess with a clock,
  Scrabble, Autonomous driving) and six rows (Observable, Deterministic,
  Episodic, Static, Discrete, Single agent), each cell filled with the
  classification (Fully / Partially, Deterministic / Stochastic, etc.).
- **Verdict:** USE.
- **Rationale:** **The most exam-critical figure in the lecture.** This
  table is exactly the kind of question that appears on the exam ("classify
  this environment along the six dimensions"). Embedded in §5 (Worked
  Examples) — environments classification.

## slide25-page-render.png

- **EXTRACTION_METHOD:** page-render (dpi=180).
- **Slide:** 25 — full slide: *Hierarchy of agent types.* Numbered list:
  (1) Table-driven, (2) Simple reflex, (3) Agents with memory, (4) Agents
  with goals, (5) Utility-based — with a "simple → complex" arrow on the
  right margin.
- **Verdict:** USE.
- **Rationale:** Visual taxonomy of agent types. Anchors §4 (Algorithms /
  Methods — Agent-type hierarchy). The "simple → complex" arrow is the
  pedagogical glue.

## slide09-page-render.png

- **EXTRACTION_METHOD:** page-render (dpi=180).
- **Slide:** 9 — full slide showing the percept-action table next to the
  vacuum-world drawing.
- **Verdict:** SKIP.
- **Rationale:** Redundant — we already use the clean table (fig07) and
  the clean vacuum-world drawing (fig05). Page-render kept on disk as
  backup but not embedded.

## fig27-xref100-slide27.png

- **Slide:** 27 — "Simple reflex agent" block diagram. Boxes: Sensors →
  *What the world is like now* → *What action I should do now* (driven by
  Condition-action rules) → Actuators. Agent box on the left, Environment
  vertical bar on the right.
- **Verdict:** USE.
- **Rationale:** The canonical Russell & Norvig block diagram of a simple
  reflex agent. Essential for §4.2.

## fig28-xref108-slide28.png

- **Slide:** 28 — "The vacuum-cleaner world" with REFLEX-VACUUM-AGENT
  pseudocode. Vacuum-world picture re-used.
- **Verdict:** SKIP.
- **Rationale:** Duplicate of fig05; the slide's pseudocode is reproduced
  verbatim in §4 of the chapter.

## fig29-xref111-slide29.png

- **Slide:** 29 — "Model-based reflex agent" block diagram. Adds an
  internal *State* box plus *How the world evolves* and *What my actions
  do* ovals to the simple-reflex diagram.
- **Verdict:** USE.
- **Rationale:** Canonical block diagram. Essential for §4.3.

## fig30-xref116-slide31.png

- **Slide:** 31 — "Goal-based agent" block diagram. Adds *What it will be
  like if I do action A* and *Goals* boxes.
- **Verdict:** USE.
- **Rationale:** Canonical block diagram. Essential for §4.4.

## fig31-xref119-slide32.png

- **Slide:** 32 — "Utility-based agent" block diagram. Adds a *How happy
  I will be in such a state* box driven by *Utility*.
- **Verdict:** USE.
- **Rationale:** Canonical block diagram. Essential for §4.5.

## fig32-xref122-slide33.png

- **Slide:** 33–36 — "Learning / Autonomous agent" block diagram. Four
  boxes: *Critic*, *Learning element*, *Performance element*, *Problem
  generator*, plus a *Performance standard* input and feedback / changes /
  learning-goals arrows.
- **Verdict:** USE.
- **Rationale:** Canonical block diagram of the learning agent (slides
  33–36 use the same image — slides 34/35/36 are just incremental call-out
  builds). Essential for §4.6.

---

## Summary

- **USE** (10 figures, all embedded in the chapter):
  - fig03 (agent ↔ environment), fig05 (vacuum world), fig07
    (percept-action table), fig27 (simple reflex), fig29 (model-based),
    fig30 (goal-based), fig31 (utility-based), fig32 (learning agent),
    `slide23-page-render.png` (environment classification table),
    `slide25-page-render.png` (agent-type hierarchy).
- **REWORK** (12 figures, all embedded with explanatory captions; the
  paired photos for each environment-property dimension):
  - fig11+fig12 (full vs partial observability), fig13+fig14 (det vs
    stoch), fig15+fig16 (episodic vs sequential), fig17+fig18 (static vs
    dynamic), fig19+fig20 (discrete vs continuous), fig21+fig22 (single
    vs multi-agent).
- **SKIP** (13 figures, justified above):
  - fig01 (title background), fig02 (WALL-E decorative), fig04 (duplicate
    of fig03), fig06 (duplicate of fig05), fig08 (dup), fig09 (dup),
    fig10 (dup), fig23 / fig24 / fig25 / fig26 (subsumed by
    slide23-page-render), fig28 (dup of fig05), `slide09-page-render`
    (subsumed by fig07 + fig05).

Total embedded in chapter = 10 USE + 12 REWORK = 22 figures.

No informative figure from the source PDF is dropped without justification.
