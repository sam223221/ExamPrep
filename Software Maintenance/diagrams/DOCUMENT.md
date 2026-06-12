# diagrams/

Pre-prepared **diagrams.net (draw.io)** files for the SB5-MAI exam, following the lecturer's advice to *prepare diagrams beforehand* (What-To-Expect p.2). Each file is uncompressed drawio XML on a single A4-landscape page: open it at [app.diagrams.net](https://app.diagrams.net) (File → Open From → Device) or in the draw.io desktop app, then edit labels/boxes during the exam to match your own feature, branch names, and class names.

All labels use course-verbatim terminology, with slide citations (e.g. `Git Lab p.11`, `ImpactAnalysis p.12`) kept inside small note/caption cells so you can keep or delete them per diagram.

## Files

| File | Content |
|---|---|
| `software-change-process.drawio` | The eight-element phased software change process: Initiation → Concept Location → Impact Analysis → Prefactoring → Actualization → Postfactoring → Conclusion, with Verification spanning Prefactoring–Conclusion; one-line annotation under each phase and the world-interaction / SC design / SC implementation grouping (SoftwareChange p.5; Lecture 12 example). |
| `git-four-areas.drawio` | Git's four areas as columns — Workspace (working dir), Index/stage, Local Repository (HEAD), Remote Repository (origin) — with command arrows: clone, add (-u), commit, push, fetch, merge, pull (= fetch + merge), checkout/restore, plus dashed diff and diff HEAD comparison lines (Git Lab p.11). |
| `github-flow-branching.drawio` | GitHub flow: main line + feature branch (`git checkout -b feature/<short-name>`), commits, push, open Pull Request, CI gate (build + tests on every PR), teammate review, merge when green. |
| `change-request-flow.drawio` | Change-request lifecycle as a Kanban board: User Story ("As a [user type], I want [goal] so that [reason]") → GitHub Issue #N → TODO backlog card → In Progress (branch + commits + PR) → Done (PR merged); the traceable chain request → backlog → branch → commits → merge. |
| `concept-location-process.drawio` | Concept location: change request (watermark example) → static route (GREP pattern matching → read code → dependency search) and dynamic route (run scenario → observe executing code, IDE debugger / Featureous) → concept located (initial class set) → feeds Impact Analysis. |
| `impact-analysis-propagation.drawio` | Impact-set marking on a JHotDraw-style interaction graph: ImageOutputFormat CHANGED (seed), SVGOutputFormat CHANGED, ExportAction PROPAGATING (mailman), Drawing UNCHANGED, SVGDrawingPanel NEXT, Figure BLANK — with a mark legend and the estimated-impact-set rule (Figure 7.9 [Raj13]). |
| `ci-pipeline.drawio` | CI pipeline on every Pull Request: PR opened (`on: pull_request`) → Checkout → Build (mvn compile) → Unit tests (mvn test) → Package (mvn package) → status-check diamond → merge gate ✓ / merge blocked ✗ with a dashed "new commit re-runs the pipeline" loop; note with the five CI principles (ContinuousIntegration p.3) and the lab's `mvn --batch-mode clean verify` (CILab p.1). |
| `refactoring-workflow.drawio` | Safe refactoring loop: identify code smell (SonarLint; Fowler catalog / SIG thresholds) → ensure green tests first (mvn clean test baseline) → apply ONE refactoring (small, IDE-automated) → re-run tests → Green? → commit with descriptive message / revert and retry in smaller steps; "one refactoring, one test run, one commit" (RefactLab p.1). |
| `clean-architecture-rings.drawio` | Clean Architecture's nested rings — Entities ⊂ Use Cases ⊂ Interface Adapters ⊂ Frameworks & Drivers — with Dependency Rule arrows pointing inward and a legend: inner = abstract/stable, outer = concrete/volatile, Boundary-interface inversion (DIP) when an inner layer needs an outer one (Clean Architecture p.7–8). |
| `testing-pyramid-aaa.drawio` | Two panels: the test pyramid — Unit (many, fast) / Integration / System–GUI (few, slow) — and the Arrange-Act-Assert strip with the deck's testLoginAdmin example (assert precondition → act → assert postcondition) (Software Testing p.8, p.33). |
| `bdd-given-when-then.drawio` | BDD pipeline: User Story → Given/When/Then scenario boxes → JGiven stage classes with @ProvidedScenarioState → @ExpectedScenarioState state flow → living documentation (JGiven HTML5 report: Successful / Failed / Pending) (BDDLab p.1). |

## Editing tips

- Replace bracketed placeholders (`[user type]`, `#N`, `feature/<short-name>`, class names) with your own project's specifics.
- Colors are meaningful: blue = process/phase boxes, orange = gates/highlighted elements, green = done/frontier, red = changed, grey = unchanged/neutral.
- Every diagram fits one A4 landscape page (1169 x 826) and prints cleanly.

## Maintenance log

- 2026-06-12 — `github-flow-branching.drawio`: edge-label offsets added (`ef3` −50px up; `Checks tab` / `checks green` +50px down) so labels no longer cover the commit/PR/CI/review boxes. `change-request-flow.drawio`: story-card citation corrected to `(ChangeInitiation p.4–5)` (3x5-card fact is p.4, story template is p.5).
