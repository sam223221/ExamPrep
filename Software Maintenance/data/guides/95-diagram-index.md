# Diagram Index — editable draw.io diagrams for the exam report

> Eleven pre-built, fully editable diagrams.net (draw.io) files live in the `diagrams/` folder of this study package. Each one is a course diagram you can open, tailor to your own lab work, export as PNG, and paste straight into the exam report. This index tells you which file to open for which exam question, what every box and arrow means, and how to adapt it on the day.

## How to use these diagrams at the exam

The lecturer explicitly recommends preparing diagrams beforehand — diagrams are a sanctioned exam aid, named alongside notes and prepared reflections in the list of allowed material (What-To-Expect p.2). The exam itself is a reflective report on your lab work (What-To-Expect p.1), and a labeled diagram is the fastest way to show a process or architecture and then reflect on it in prose.

All eleven files live in the `diagrams/` folder at the root of this study package. They are uncompressed draw.io XML, so they open and edit cleanly: go to app.diagrams.net (File → Open From → Device) or use the draw.io desktop app, click any box or arrow label to rewrite it, then File → Export as → PNG to get an image you can paste into the report. Every diagram fits one A4 landscape page. Before the exam, do a dry run: open one file, rename a class to one from your own JHotDraw fork, and export it — the whole loop takes under two minutes.

The eleven files: `software-change-process.drawio`, `git-four-areas.drawio`, `github-flow-branching.drawio`, `change-request-flow.drawio`, `concept-location-process.drawio`, `impact-analysis-propagation.drawio`, `ci-pipeline.drawio`, `refactoring-workflow.drawio`, `clean-architecture-rings.drawio`, `testing-pyramid-aaa.drawio`, `bdd-given-when-then.drawio`.

General tailoring rule: replace every bracketed placeholder (`[user type]`, `#N`, `feature/<short-name>`, the JHotDraw class names) with the specifics from your own repository, and delete the small grey citation notes if you do not want slide references visible in the exported image. A diagram that names *your* classes, *your* branch, and *your* pipeline reads as evidence; a generic one reads as decoration (What-To-Expect p.5).

## Software change process diagram — eight phases from smelly repository to SOLID repository

### What it shows

The master phased software change process as one left-to-right pipeline: a grey **Repository with Bad Code Smells** box feeds **Initiation → Concept Location → Impact Analysis → Prefactoring → Actualization → Postfactoring → Conclusion**, ending in a grey **SOLID Repository** box (SoftwareChange p.5). A yellow **Verification** banner sits above the row, spanning Prefactoring through Conclusion — testing and walkthroughs run alongside the whole implementation half. Under each phase box is a one-line italic annotation saying what that phase is for ("find WHERE to change", "determine the impact set", "refactor BEFORE the change", and so on), and a bottom strip groups the phases into *world interaction*, *SC design*, and *SC implementation*.

### Use it in the report when

- Any question asks you to describe the overall software change process, the change mini-cycle, or how your lab work followed a disciplined process — this is the course's spine diagram (SoftwareChange p.5).
- You open the report with an overview section: paste this once, then reference its phases ("during Concept Location I…", "in Postfactoring I…") in every later section.
- You need to explain *where* a specific activity belongs — e.g. why refactoring happened both before (Prefactoring) and after (Postfactoring) the actual code change.
- You want to show that Verification is not a final phase but a parallel activity spanning Prefactoring through Conclusion.

### Key elements explained

- **Repository with Bad Code Smells / SOLID Repository** — the before and after states; a change is a transformation of the codebase's quality, not just its behavior (Lecture 12 worked example).
- **Initiation** — capture and prioritize the change request, the world-interaction entry point (SoftwareChange p.5).
- **Concept Location** — find WHERE in the code the change must happen (ConceptLocation p.6).
- **Impact Analysis** — determine the full impact set before touching anything (ImpactAnalysis p.12).
- **Prefactoring / Actualization / Postfactoring** — refactor to prepare, create and plug in the new code, then refactor again to remove anti-patterns introduced by the change.
- **Conclusion** — commit and build the new baseline, the closing world interaction.
- **Verification banner** — testing plus walkthroughs running vertically alongside the implementation phases (SoftwareChange p.5).

### File & how to edit

The software change process diagram (the eight-phase pipeline Initiation → Concept Location → Impact Analysis → Prefactoring → Actualization → Postfactoring → Conclusion with the parallel Verification banner) lives at `diagrams/software-change-process.drawio` — an editable, uncompressed draw.io XML file you can open in diagrams.net or the draw.io desktop app. Tailoring tip: keep the eight phase boxes verbatim (they are course terminology) but rewrite the italic annotation under each phase into one line about what *you* did there in your lab change — that single edit turns the theory diagram into a narrative of your own work.

## Git four areas diagram — workspace, stage, local repository, remote origin

### What it shows

Git's four storage areas as four tall columns: **1. Workspace** (working dir, your editable files), **2. Index / stage** (what the next commit will contain), **3. Local Repository** (committed history, HEAD), and **4. Remote Repository** (origin — the shared fork on GitHub), the remote column tinted orange to mark it as the only shared area (Git Lab p.11). Labeled command arrows run between the columns: `clone`, `add (-u)`, `commit`, `push`, `fetch`, `merge`, `pull` (= fetch + merge in one step), and `checkout / restore`. Two dashed, arrowhead-free comparison lines show `diff` (workspace vs index, unstaged edits) and `diff HEAD` (workspace vs last commit). A caption note states the key insight: commit is local — teammates see nothing until you push.

### Use it in the report when

- A question asks how you used version control, Git, or GitHub during the labs — this diagram lets you explain any command by pointing at which areas it moves data between (Git Lab p.11).
- You reflect on collaboration: why a teammate could not see your commits until you pushed, or why `pull` sometimes produced merge conflicts (pull = fetch + merge).
- You justify your staging habits — e.g. why you used `git add -u` and `git diff` before committing, to control exactly what entered each commit.

### Key elements explained

- **Workspace** — the files you actually edit; the only area your editor touches.
- **Index / stage** — the staging area; `add` copies changes here, defining the next commit's content (Git Lab p.11).
- **Local Repository (HEAD)** — the committed history on your machine; `commit` records the staged snapshot here.
- **Remote Repository (origin)** — the GitHub fork; `push` publishes, `fetch` downloads without touching the workspace, `clone` makes the initial full copy.
- **pull = fetch + merge** — the one-step shortcut, and the reason pulling can trigger a merge.
- **diff vs diff HEAD** — unstaged-only changes versus everything since the last commit (staged + unstaged).

### File & how to edit

The Git four areas diagram (workspace, index/stage, local repository, and remote origin columns with the clone / add / commit / push / fetch / merge / pull command arrows) lives at `diagrams/git-four-areas.drawio` — an editable, uncompressed draw.io XML file you can open in diagrams.net. Tailoring tip: the arrow labels are plain text — append your own real example after a command (e.g. "push — publish commits — used after every refactoring step on `feature/refactor-smells`") so the diagram cites your actual workflow.

## GitHub flow branching diagram — feature branch, pull request, CI gate, merge to main

### What it shows

The GitHub-flow branching model as two horizontal lanes: a **main** lane with commits M1, M2 and a green **merge commit**, and a **feature/`<short-name>`** lane below it (IntroLab p.1; Git Lab p.5). An arrow labeled `git checkout -b feature/<short-name>` branches off M1 into commits 1–3 on the feature lane; `git push -u origin feature/<short-name>` leads to an **Open Pull Request into main** box, then into an orange **CI GATE** box ("checks run: build + tests on every PR", CILab p.1), then **Teammate reviews the PR**, and finally a "merge when green" arrow back up into the merge commit on main. A note records the policy: main stays releasable at all times; unfinished work lives only on branches; one feature branch per member.

### Use it in the report when

- A question asks about your branching strategy, team workflow, or how changes reached main — this is the workflow diagram for the whole semester's repository work (Git Lab p.5, p.11).
- You explain why main was always releasable, or why every change went through a pull request and review instead of direct commits.
- You connect version control to CI: the CI gate box is where your pipeline (see the CI pipeline diagram) plugs into the branching model (CILab p.1).

### Key elements explained

- **main lane** — the always-releasable line; only merge commits from reviewed, green PRs land here.
- **feature/`<short-name>`** — the per-change branch naming convention; one feature branch per member (IntroLab p.1).
- **commit 1–3** — small commits on the branch; unfinished work is isolated from main.
- **Open Pull Request into main** — the integration request that triggers checks and review.
- **CI GATE — build + tests on every PR** — GitHub Actions runs the build and the test suite on the PR's Checks tab before anyone may merge (CILab p.1).
- **Teammate reviews the PR / merge when green** — human review after machine checks; merging requires both.

### File & how to edit

The GitHub flow branching diagram (main lane, feature/`<short-name>` branch lane, pull request, CI gate, and merge-when-green commit) lives at `diagrams/github-flow-branching.drawio` — an editable, uncompressed draw.io XML file you can open in diagrams.net. Tailoring tip: rename `feature/<short-name>` to a real branch from your fork (e.g. `feature/export-watermark`) and relabel commit 1–3 with your actual commit subjects — the diagram then doubles as evidence that your repository followed the model (What-To-Expect p.5).

## Change request flow diagram — user story, GitHub issue, Kanban board lifecycle

### What it shows

The full lifecycle of a change request, drawn as a story card flowing onto a Kanban board. At the top, a yellow **User Story (3x5 card)** box with the template "As a [user type], I want [some goal] so that [some reason]" (ChangeInitiation p.5) feeds a **GitHub Issue #N** box (feature, bug fix, or improvement — Git Lab p.19). Below, three swimlanes: **TODO — product backlog** (the story card linked to Issue #N, with Must / Nice-to-have / Won't-have priority), **In Progress** (three cards: `git checkout -b feature/<short-name>`, small commits referencing #N with messages explaining WHY, then push branch + open Pull Request + CI builds the PR), and **Done** (PR reviewed and merged into main). A note states the traceable chain: request → backlog → branch → commits → merge (ChangeReqLab p.1).

### Use it in the report when

- A question asks how a change request was initiated, tracked, or managed — this covers the Initiation phase and the Change Request lab end to end (ChangeInitiation p.5; ChangeReqLab p.1).
- You reflect on traceability: how a reader can follow your user story to its issue, branch, commits, and merge in the graded repository (What-To-Expect p.5).
- You explain prioritization (Must / Nice-to-have / Won't have) or why commits referenced the issue number.

### Key elements explained

- **User Story card** — the course's request format: "As a [user type], I want [some goal] so that [some reason]" (ChangeInitiation p.5).
- **GitHub Issue #N** — the recorded, numbered request; the anchor every commit references (Git Lab p.19).
- **TODO / product backlog** — the prioritized wish list; cards wait here until work starts (ChangeReqLab p.1).
- **In Progress cards** — branch creation, small commits referencing #N whose messages explain WHY, and the PR that CI builds.
- **Done** — the PR merged into main; the card moves only when the chain is complete.

### File & how to edit

The change request flow diagram (user story card → GitHub Issue #N → Kanban board with TODO / In Progress / Done swimlanes) lives at `diagrams/change-request-flow.drawio` — an editable, uncompressed draw.io XML file you can open in diagrams.net. Tailoring tip: replace `[user type]`, `[goal]`, `[reason]`, and `#N` with your actual lab user story and issue number, so the exported board shows the real traceable chain from your repository.

## Concept location process diagram — static grep route and dynamic debugger route

### What it shows

How a change request becomes a located concept in the code. A yellow start box ("Change request: concept to locate", with the course's watermark example — Export, Drawing, Text, Format — ConceptLocation p.6) splits into two routes. The **STATIC SEARCH** route (code does not run): **Pattern matching: GREP** (query → investigate → refine) → **Read candidate code** (partial comprehension) → **Dependency search** following the class dependency graph. The **DYNAMIC SEARCH** route (execution traces, program runs): **Run the program** exercising the feature scenario → **Observe which code executes** (IDE debugger — CLLab; Featureous [Ols12a]). Both routes converge on a green **Concept located: initial class set** box, which feeds an orange **Impact Analysis — seeds marked CHANGED** box (AnalysisLab p.1). A note lists the four methodology families: human knowledge, traceability tools, dynamic search, static search (ConceptLocation p.7–8).

### Use it in the report when

- A question asks how you found WHERE to make your change — concept location is the "find the place" phase and this diagram is its method map (ConceptLocation p.6–8).
- You justify your search choice: e.g. why you used the debugger (dynamic) instead of only grep (static), or how grep's query → investigate → refine loop narrowed candidates.
- You hand over to impact analysis: the located classes become the seeds marked CHANGED (AnalysisLab p.1).

### Key elements explained

- **Pattern matching / GREP** — static keyword search over the source; iterate query → investigate → refine (ConceptLocation p.7–8).
- **Read candidate code** — partial comprehension only; you read just enough to confirm or reject a candidate.
- **Dependency search** — walk the class dependency graph from a known class toward the concept.
- **Run the program / observe** — dynamic search: exercise the feature scenario and watch which code executes, with the IDE debugger (CLLab) or a tool like Featureous [Ols12a].
- **Concept located: initial class set** — the output artifact: the domain classes and responsibilities where the change starts.

### File & how to edit

The concept location process diagram (the static grep route and the dynamic debugger route converging on the located class set, then feeding impact analysis) lives at `diagrams/concept-location-process.drawio` — an editable, uncompressed draw.io XML file you can open in diagrams.net. Tailoring tip: swap the watermark example in the start box for your own change request, and list the classes you actually found in the green "concept located" box.

## Impact analysis propagation diagram — CHANGED, PROPAGATING, NEXT marks on the interaction graph

### What it shows

A mid-walk snapshot of impact analysis on a JHotDraw-style class interaction graph, following the marking algorithm of Figure 7.9 in [Raj13] (ImpactAnalysis p.12). Six class boxes carry marks: **ImageOutputFormat — CHANGED (seed)** in red, **SVGOutputFormat — CHANGED** in red, **ExportAction — PROPAGATING (mailman)** in orange, **Drawing — UNCHANGED** in grey, **SVGDrawingPanel — NEXT (frontier)** in green, and **Figure — BLANK (not yet reached)** in white, with undirected interaction edges between them. A five-swatch legend defines each mark, and the caption states the result rule: the estimated impact set = all classes marked CHANGED or PROPAGATING → {ImageOutputFormat, SVGOutputFormat, ExportAction}; the walk ends when no class is marked NEXT.

### Use it in the report when

- A question asks how you determined the impact of your change, or how you knew which classes to inspect — this is the Analysis Lab's core procedure (AnalysisLab p.1; Figure 7.9 [Raj13]).
- You explain a specific mark decision: why a class was PROPAGATING rather than UNCHANGED, and what missing that mark would have cost (an under-estimated impact set and a future regression).
- You report your estimated impact set and want to show the rule that produced it (ImpactAnalysis p.12).

### Key elements explained

- **CHANGED (red)** — the class needs edits; the seed comes straight from concept location (ImpactAnalysis p.12).
- **PROPAGATING (orange)** — the mailman: relays the change between neighbors without needing edits itself; keeps the search going past conduits (ImpactAnalysis p.10).
- **NEXT (green)** — the frontier: scheduled for inspection; the walk terminates when no NEXT remains.
- **UNCHANGED / INSPECTED (grey)** — inspected and judged unaffected.
- **BLANK (white)** — not yet reached by the walk.
- **Estimated impact set** — everything marked CHANGED or PROPAGATING when the walk ends (Figure 7.9 [Raj13]).

### File & how to edit

The impact analysis propagation diagram (the class interaction graph with CHANGED / PROPAGATING / NEXT / UNCHANGED marks and the estimated-impact-set rule) lives at `diagrams/impact-analysis-propagation.drawio` — an editable, uncompressed draw.io XML file you can open in diagrams.net. Tailoring tip: rename the six class boxes to the classes from YOUR impact analysis (keep the marks and colors), so the exported snapshot documents your actual walk rather than the textbook example.

## CI pipeline diagram — PR trigger, build, test, merge gate

### What it shows

The continuous integration pipeline that GitHub Actions runs on every pull request (CILab p.1). A green start ellipse **Pull Request opened** (trigger: `on: pull_request`) flows through four stage boxes: **Checkout** (actions/checkout — the runner gets code from the repo) → **Build** (`mvn compile`) → **Unit tests** (`mvn test` — self-testing build) → **Package** (`mvn package`), then into an orange **Status check: build green?** decision diamond. The green branch leads to **Merge gate on main ✓** (branch protection requires the status check to pass — PR can merge); the red branch leads to **Merge blocked ✗** (fix and push a new commit), with a dashed loop back to Checkout labeled "new commit re-runs the pipeline". A yellow note lists the five CI principles (ContinuousIntegration p.3) and the lab's actual one-command pipeline: `mvn --batch-mode clean verify` (CILab p.1).

### Use it in the report when

- The report asks "How did you create your pipeline?" — the final question in the lecturer's example report and a named important topic (What-To-Expect p.4, p.6). Paste this, then narrate each stage of your workflow file.
- You explain why a red build blocked a merge, and how pushing a fix re-ran the checks.
- You connect practice to theory: map your workflow to the five CI principles, especially "make the build self-testing" and "build every commit" (ContinuousIntegration p.3).

### Key elements explained

- **Trigger `on: pull_request`** — the workflow runs on every PR, so broken code is caught before merge (CILab p.1).
- **Checkout** — actions/checkout puts the PR's code on the runner.
- **Build (`mvn compile`) / Unit tests (`mvn test`) / Package (`mvn package`)** — the Maven phases; the test stage is what makes the build self-testing (ContinuousIntegration p.3).
- **Status check diamond** — the pass/fail verdict GitHub shows on the PR's Checks tab.
- **Merge gate ✓ / Merge blocked ✗** — branch protection requires the status check; red means fix and push, which re-runs the pipeline.
- **`mvn --batch-mode clean verify`** — the lab pipeline's single command that runs all phases (CILab p.1).

### File & how to edit

The CI pipeline diagram (the continuous integration flowchart: pull-request trigger → checkout → build → unit tests → package → status-check merge gate) lives at `diagrams/ci-pipeline.drawio` — an editable, uncompressed draw.io XML file you can open in diagrams.net. Tailoring tip: relabel the stage boxes to match the exact step names in your own `.github/workflows/` YAML file, so diagram and repository tell the same story (What-To-Expect p.5).

## Refactoring workflow diagram — code smell, green tests, one refactoring, commit

### What it shows

The safe refactoring loop — measure → refactor → verify (RefactLab p.1). The flow runs: **Identify code smell** (SonarLint plus your change-request scope; name it from the Fowler catalog / SIG thresholds) → **Ensure green tests first** (`mvn clean test` — the safety-net baseline) → **Apply ONE refactoring** (small step, IDE-automated, e.g. Extract Method) → **Re-run tests** (`mvn test`) → a **Green?** decision diamond. Green leads to **Commit with descriptive message** (the example: "Extract Method: selectionBounds() out of drawSelection (Long Method, G1)") and loops back to the next smell; red leads to **Revert / fix the step** (behaviour must be preserved) with a dashed "retry in smaller steps" loop back to the refactoring box. A note carries the discipline: one refactoring, one test run, one commit — "a series of small behavior preserving transformations" (RefactLab p.1).

### Use it in the report when

- Theory questions like "How do you identify a code smell?" or "What is meant by a refactoring pattern?" appear — both are the lecturer's named example questions (What-To-Expect p.3, p.6); the diagram shows where identification and the catalog pattern sit in the loop.
- You narrate your refactoring lab work: which smell, which catalog refactoring, and how tests proved behaviour preservation (RefactLab p.1).
- You justify commit granularity — why each refactoring got its own commit with the smell and refactoring named in the message.

### Key elements explained

- **Identify code smell** — detection via SonarLint plus your own reading, named against the Fowler catalog or SIG thresholds (RefactLab p.1).
- **Ensure green tests first** — refactoring without a green baseline cannot prove behaviour preservation; `mvn clean test` establishes the safety net.
- **Apply ONE refactoring** — one small, ideally IDE-automated step (e.g. Extract Method); never batch transformations.
- **Green? → Commit / Revert** — green means commit with a descriptive message naming the refactoring and smell; red means revert and retry in smaller steps.
- **Behavior-preserving transformations** — the definition of refactoring itself: external behaviour unchanged, structure improved (RefactLab p.1).

### File & how to edit

The refactoring workflow diagram (the safe loop: identify code smell → green tests first → apply ONE refactoring → re-run tests → commit or revert) lives at `diagrams/refactoring-workflow.drawio` — an editable, uncompressed draw.io XML file you can open in diagrams.net. Tailoring tip: rewrite the example commit-message box with one of YOUR real refactoring commits (smell name, refactoring name, class) — it becomes a ready-made evidence exhibit for the report.

## Clean architecture rings diagram — Entities, Use Cases, Interface Adapters, Frameworks and the Dependency Rule

### What it shows

Clean Architecture's concentric layers as four nested rounded rectangles: **Frameworks & Drivers** (UI / DB / Web / Devices) on the outside, then **Interface Adapters** (Controllers / Presenters / Gateways), then **Use Cases** (Application Business Rules), with **Entities** (Enterprise Business Rules) innermost (Clean Architecture p.7–8). Two bold arrows labeled "dependencies point inward" and "Dependency Rule" run from the outer ring to the core. A yellow legend explains the rule: source-code dependencies point only inward; inner layers are abstract, general, and rarely change, outer layers are concrete, specific, and change frequently; and if an inner layer seems to need an outer one, invert the dependency — declare an interface (Boundary) in the inner layer and implement it in the outer layer (DIP).

### Use it in the report when

- The report asks about clean architecture concepts or how you applied them to your code — a named important topic, and the lecturer specifically suggested attaching the clean-architecture diagram with the four layers labeled with classes from your project (What-To-Expect p.4–5).
- You explain a design decision from the Actualization lab: which layer your new code went into and why.
- You discuss maintainability: why stable business rules must not depend on volatile frameworks (Clean Architecture p.8).

### Key elements explained

- **Entities (Enterprise Business Rules)** — innermost, most abstract, most stable; least reason to change (Clean Architecture p.7–8).
- **Use Cases (Application Business Rules)** — application-specific orchestration of entities.
- **Interface Adapters (Controllers / Presenters / Gateways)** — translate between the use cases and the outside world's formats.
- **Frameworks & Drivers (UI / DB / Web / Devices)** — outermost, most concrete, most volatile; mere details from the core's perspective.
- **Dependency Rule** — source-code dependencies point only inward (Clean Architecture p.8).
- **Boundary interface / DIP** — the dependency-inversion escape hatch when an inner layer needs outer-layer services: interface declared inside, implemented outside.

### File & how to edit

The clean architecture diagram (the concentric rings Entities, Use Cases, Interface Adapters, Frameworks & Drivers with the inward-pointing Dependency Rule arrows) lives at `diagrams/clean-architecture-rings.drawio` — an editable, uncompressed draw.io XML file you can open in diagrams.net. Tailoring tip: add your own JHotDraw class names inside each ring (e.g. where your changed classes sit) — that labeling exercise is exactly what the lecturer recommended preparing (What-To-Expect p.4).

## Testing pyramid diagram — unit, integration, system levels with Arrange-Act-Assert

### What it shows

Two side-by-side panels (Software Testing p.8, p.33). Left: the test pyramid as three stacked levels — a wide green **Unit tests** base (many, fast — a single code-path through a single method; mocks/stubs replace dependencies), a yellow **Integration tests** middle (already-unit-tested components working together across their interfaces), and a narrow red **System / GUI tests** top (few, slow — the whole system end-to-end against its specification), captioned "each level catches a different class of fault — use all three". Right: the **Arrange-Act-Assert (AAA)** pattern as three boxes using the deck's `testLoginAdmin` example — Arrange (set up the fixture and assert the precondition, `assertFalse(libApp.adminLoggedIn())`), Act (perform the action, `boolean login = libApp.adminLogin("adminadmin")`), Assert (assert the postcondition, `assertTrue(login); assertTrue(libApp.adminLoggedIn())`).

### Use it in the report when

- A question asks about your testing strategy or test levels — use the pyramid to place your JUnit tests (unit) and JGiven scenarios (higher level) and argue the many-fast/few-slow trade-off (Software Testing p.8).
- You walk through one of your own unit tests: structure the prose as Arrange, Act, Assert and point at the three parts in your code (Software Testing p.33).
- You justify mocks/stubs: why unit tests replaced dependencies to stay fast and isolated.

### Key elements explained

- **Unit tests (many, fast)** — one code-path through one method; dependencies replaced by mocks/stubs (Software Testing p.8).
- **Integration tests** — verify already-unit-tested components cooperating across their interfaces.
- **System / GUI tests (few, slow)** — exercise the whole system end-to-end against its specification.
- **Arrange** — build the fixture and assert the precondition, so a failure can be blamed on the action, not the setup (Software Testing p.33).
- **Act** — the single action under test.
- **Assert** — the postcondition checks that define pass/fail.

### File & how to edit

The testing pyramid diagram (unit / integration / system test levels side by side with the Arrange-Act-Assert pattern strip) lives at `diagrams/testing-pyramid-aaa.drawio` — an editable, uncompressed draw.io XML file you can open in diagrams.net. Tailoring tip: replace the `testLoginAdmin` example in the AAA strip with the Arrange/Act/Assert lines from one of YOUR committed tests — the diagram then references the graded repository directly (What-To-Expect p.5).

## BDD Given-When-Then diagram — user story to JGiven stages and living documentation

### What it shows

The full BDD pipeline (BDDLab p.1) in four columns. A purple **User Story** card ("As a [user type], I want [some goal] so that [some reason]") maps to a concrete worked example: the **Given [precondition]** (context set-up only, with concrete data), **When [action]** (one logical triggering action per scenario), and **Then [outcome]** (expected outcome — where the assertion lives) boxes. Dashed arrows automate each part with JGiven stage classes: **GivenStage** with `@ProvidedScenarioState` (provides the state), **WhenStage** with `@ExpectedScenarioState` (consumes), acts, and `@ProvidedScenarioState` (result), and **ThenStage** with `@ExpectedScenarioState`, asserting with AssertJ (void step). Vertical arrows show state flowing between stages matched by type (`@ProvidedScenarioState` → `@ExpectedScenarioState`). Finally, `mvn test` renders the scenario back as prose in a purple **Living documentation** box — the JGiven HTML5 report (Successful / Failed / Pending).

### Use it in the report when

- A question asks about behavior-driven development, acceptance testing, or your JGiven scenarios — this diagram covers the BDD lab end to end (BDDLab p.1).
- You explain how a user story became an executable specification: story → Given/When/Then → stage classes → report.
- You discuss verification beyond unit tests: living documentation as evidence that the system meets the story, readable by non-programmers.

### Key elements explained

- **User Story** — the same "As a [user type]…" template as change initiation; BDD starts from the request (BDDLab p.1).
- **Given / When / Then** — precondition set-up with concrete data, one logical triggering action, and the asserted outcome.
- **GivenStage / WhenStage / ThenStage** — JGiven's one-class-per-part implementation pattern.
- **`@ProvidedScenarioState` → `@ExpectedScenarioState`** — how state flows between stage classes, matched by type.
- **AssertJ in ThenStage** — assertions live only in Then, as void steps.
- **Living documentation** — the JGiven HTML5 report rendering scenarios as prose with Successful / Failed / Pending status.

### File & how to edit

The BDD Given-When-Then diagram (user story → Given / When / Then boxes → JGiven stage classes → living documentation pipeline) lives at `diagrams/bdd-given-when-then.drawio` — an editable, uncompressed draw.io XML file you can open in diagrams.net. Tailoring tip: fill the Given/When/Then boxes with the actual scenario text from one of your committed JGiven tests, and put your real stage class names in the three stage boxes.
