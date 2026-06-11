# MCQ Topic Taxonomy & Lecture Map

> The controlled vocabulary, the lecture→topic map, and the difficulty scale that
> govern every MCQ and guide tag in the SB5-MAI study package.

## Controlled Topic Vocabulary

The closed list below contains the **only** allowed values for the `topic` field on
an MCQ and for guide tags. Use the strings exactly as written (same casing and
spacing). Do not invent new topics; if a question spans two, pick the dominant one
and add the second via `tags`.

- Software Change Process
- Concept Location
- Impact Analysis
- Refactoring
- Prefactoring
- Actualization
- Clean Architecture
- OO Principles
- Clean Code
- Design Patterns
- Software Testing
- BDD / Verification
- Technical Debt
- Software Processes / CI
- Version Control / Git
- JHotDraw Case Study

## Lecture → Primary Topics

Each content-bearing lecture maps to 1–3 primary topics drawn from the controlled
vocabulary above. (Lectures 8 and 12 have no material and are omitted.)

| Lecture | Title | Primary topics |
|---------|-------|----------------|
| L01 | Introduction & Version Control | Version Control / Git, Software Change Process |
| L02 | Software Change & Concept Location (introduces JHotDraw) | Software Change Process, Concept Location, JHotDraw Case Study |
| L03 | Impact Analysis, Software Processes & CI | Impact Analysis, Software Processes / CI |
| L04 | Refactoring & Maintainable Code | Refactoring, Prefactoring |
| L05 | Actualization, Clean Architecture & OO Principles | Actualization, Clean Architecture, OO Principles |
| L06 | Clean Code & Design Patterns | Clean Code, Design Patterns |
| L07 | Software Testing | Software Testing |
| L09 | BDD & Verification | BDD / Verification |
| L10 | Conclusion & Worked Example (Drawlets) | Software Change Process, JHotDraw Case Study |
| L11 | Technical Debt | Technical Debt |

## Difficulty Scale

The `difficulty` field on every MCQ takes exactly one of these values (matches the
MCQ schema):

- **easy** — Recall of a single definition or fact; one obviously-correct option, weak distractors.
- **medium** — Apply a concept or distinguish two related ideas; distractors are plausible but resolvable from the guide.
- **hard** — Multi-step reasoning, comparing several concepts, or applying a process phase to a concrete JHotDraw/Drawlets scenario; distractors target common misconceptions.
- **very-hard** — Synthesis across lectures or subtle edge cases (e.g. ordering the full change-process spine, telling prefactoring from postfactoring in context); every distractor is individually defensible and must be reasoned out.
