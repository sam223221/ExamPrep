# Lecture 1: Introduction to Software Architecture — Definitions, Terminology, Structures, and Principles

> **Source:** lecture_1.pdf (84 pages)
> **Lecturer:** Jukka Ruohonen
> **Date (as stated):** February 10, 2026 (course code T630019402)

## Themes covered

- What "software architecture" actually means (and what it is NOT)
- Software architecture vs. detailed design vs. implementation
- Quality attributes and the role of trade-offs ("tensions")
- The Twin Peaks model: requirements and architecture co-evolve
- A working vocabulary: modules, components, connectors, interfaces, processes, machines, systems, deployments, environments, elements
- Component structures vs. module structures (and layered structures)
- Architectural views and viewpoints (including Kruchten's 4+1)
- Design principles for components: substitution (Liskov-style), cohesion, segregation, single responsibility, open-closed, no vendor lock-in
- System architecture vs. enterprise architecture
- Who the software architect is — communication-heavy, senior role

## Concepts

### Software architecture (the working definition)
**Definition:** A software architecture is the set of structures needed to reason about a computing system; these structures comprise software *elements*, *relations* among them, and *properties* of both (Clements et al. 2010, quoted via Fairbanks 2010).
**Why it matters:** This is the definition the whole course is built on. Every later concept — quality attributes, views, tactics, patterns — bottoms out in "elements + relations + properties."
**Detailed explanation:** Notice three things in the definition. First, architecture is *plural* — there is no single picture of a system, but many structures (component, module, deployment, etc.) each chosen to answer a particular question. Second, it is for *reasoning*, not for documentation alone — if a diagram does not help you predict or argue about system behavior, it is not architectural. Third, "properties" are first-class — modules and their connections matter, but so do attributes like latency, availability, and modifiability that the structure *gives rise to*.
**Analogy:** A city is not its skyline photo. To reason about traffic you use a road map; to reason about power outages, an electrical grid map; to reason about flood risk, a topographic map. Each map is a *structure* — a deliberate choice of elements (intersections, substations, contour lines), relations (roads, lines, gradients), and properties (capacity, voltage, elevation). The "architecture" of the city is the whole bundle of these maps used to reason about the city; no single map is "the architecture."
**Example:** For the running flight-and-hotel reservation system the lecture sketches several views: a UML-style component diagram, a less formal "pseudo component diagram," and a cloud-internet view. None of them alone is "the" architecture; together they let different stakeholders reason about the system.
**Common pitfall / nuance:** Students often conflate the architecture with a single diagram (usually the boxes-and-arrows one). The lecturer's terminology is sharper: *structures* are what live in the head/repository, *views* are the diagrams that represent them.
**Related diagram:** `![Concepts: components, modules, connectors, interfaces](../images/lecture_1/lecture_1_p40_img1_concepts_components_modules_connectors.png)`

### Six truisms about software architecture (Bass et al.)
**Definition:** Six baseline facts the lecture asserts at the start: (1) architecture is an abstraction; (2) it is engineering, not art; (3) it is software design, but not all software design is architecture; (4) every system has an architecture (even an accidental one); (5) not all architectures are good; (6) architectures usually have *both* requirements and constraints, plus needed domain expertise.
**Why it matters:** These set the tone for the entire course. They block several common student moves: "I just picked a stack, that's the architecture" (false — #2, #5), "small projects have no architecture" (false — #4), "architecture is just personal style" (false — #2).
**Detailed explanation:** "Engineering not art" is the most loaded one. Ruohonen uses Sydney Opera House (admired but famously over-budget and behind schedule) vs. brutalist concrete buildings (often ugly but functional and budget-respecting) to argue that *fit-for-purpose under constraints* matters more than visual elegance. Truism #3 is the boundary against "detailed design": architectural decisions are the macroscopic ones — modules and how they connect — leaving the rest (algorithms, internal data structures, single-class layouts) to detailed design. Truism #4 is sneaky: even a hacked-together prototype has an architecture; the only question is whether it was chosen or accreted.
**Analogy:** A bridge built without an engineer still has a structural design — gravity will reveal it when the bridge collapses. Same with software: skipping architectural thinking does not get you out of having an architecture; it only guarantees a bad one.
**Example:** The lecturer's "Not Like This" slides juxtapose the Sydney Opera House (architecture-as-art), a brutalist building (architecture-as-pragmatic-engineering), and a chaotic pseudo-scientific diagram (architecture-as-mess) to make the point visually.
**Common pitfall / nuance:** Don't read truism #2 as "boring is good." It means "answer the right engineering questions under real constraints." Aesthetic clarity in a diagram is itself an engineering virtue (communication, knowledge transfer).

### Software design, software architecture, and implementation
**Definition:** Three layers of decision-making: *design* is the broadest umbrella; *architecture* is the macroscopic subset of design that fixes the system's structure and quality attributes; *implementation* is the line-by-line realization. Between every pair lie *tensions* driven by requirements, constraints, domain knowledge, and quality attributes.
**Why it matters:** The exam will ask trade-off questions ("how do you settle tensions among different qualities in a concrete design?"). This three-layer picture is the mental model for placing each decision.
**Detailed explanation:** Fairbanks (2010) sharpens the division: architecture covers macroscopic parts and their connections; detailed design covers everything else. Architecture *constrains* implementation in both good ways (clear seams, predictable performance) and bad ways (rigidity, hard-to-change decisions). The decisions you make architecturally are by definition the ones you cannot easily reverse later — that is what makes them architectural.
**Analogy:** Building a house: architecture is the floor plan and where the load-bearing walls go; detailed design is the kitchen cabinet layout; implementation is the actual carpentry. You can repaint a wall (implementation) cheaply. You can re-tile a kitchen (detailed design) with effort. Moving a load-bearing wall (architecture) costs you the project.
**Example:** "Healthcare emergency system must be available 24/7/365" is a requirement that pushes architecture toward redundancy and replication. "Team has no healthcare experience" is a constraint that pushes toward simpler patterns. "Budget is fixed by public procurement" is a constraint that limits hardware. These three tensions are settled architecturally, *before* anyone writes code.
**Common pitfall / nuance:** Don't equate "architecture" with "UML diagrams produced upfront." Architecture is the set of *decisions about hard-to-change structure*; the diagrams document those decisions.
**Related diagram:** `![Design, architecture, implementation with tensions](../images/lecture_1/lecture_1_p28_img1_design_arch_implementation_pyramid.png)`

### Quality attributes
**Definition:** Non-functional properties of a system (availability, performance, modifiability, security, scalability, usability, etc.) that the architecture is designed to fulfill. They derive from non-functional requirements, constraints, and domain knowledge.
**Why it matters:** Architectures are evaluated by *prioritized* quality attributes, not by whether they "do the feature." Functional requirements ("the system reserves a flight") matter less to the architect than non-functional ones ("the system is available 99.99% of the time").
**Detailed explanation:** Quality attributes almost always conflict — more security usually means worse performance; more modifiability usually means more upfront complexity. The architect's job is to *prioritize* and then choose tactics and patterns that emphasize the top-ranked attributes while not sacrificing the others below acceptable thresholds. An architecture also enables *incremental implementation*: a good one lets you build piece by piece instead of integrating everything at once.
**Analogy:** Ordering a car. Functional requirements: it must drive, brake, signal. That tells you nothing about whether to buy a Ferrari, a Volvo, or a Hilux. The interesting decisions are non-functional: top speed (performance), crash safety (reliability), repairability (modifiability), fuel cost (efficiency). You can't maximize all of them; you rank what you care about and accept trade-offs.
**Example:** The lecturer's case: "availability of utmost importance" — that single prioritization changes the architecture from a single VM to redundant deployments across regions, even though the *feature list* never mentions availability.
**Common pitfall / nuance:** Students list quality attributes flatly. The lecture insists on *prioritization* — without a ranking, an architecture cannot be evaluated, because every architecture is good at *something* and bad at something else.

### Constraints (two flavors)
**Definition:** Constraints are limits the architect did not get to choose. They fall in two places: constraints that flow *into* the architecture (budget, regulations, hardware, team skills) and constraints the architecture *imposes on* the implementation (chosen stack, allowed connectors, deployment model).
**Why it matters:** The architect's freedom is bounded on both sides. Recognizing which constraints come from above (given) and which you are creating (your decision becomes someone else's given) is the discipline of architecture.
**Detailed explanation:** "We must use Java because the rest of the company uses Java" is an incoming constraint. "Modules in this system must talk only via REST" is a constraint *you* imposed — it constrains the implementers, and you own its consequences. Constraints can "inhibit" (rule things out) or "exhibit" (enforce certain qualities).
**Analogy:** A composer writing a symphony is constrained by the instruments in the orchestra (incoming). But once they write "string quartet only" in bar 32, every subsequent musician has a new constraint they did not choose (outgoing).
**Example:** Healthcare emergency system: public procurement caps the budget (incoming); the architect then forbids vendor-specific cloud services to avoid lock-in (outgoing constraint on the implementers).
**Common pitfall / nuance:** Don't mistake constraints for requirements. A requirement says "the system shall…"; a constraint says "the system cannot…" or "the system must use…". They both shape the design but they enter the problem differently.
**Related diagram:** `![Two types of constraints](../images/lecture_1/lecture_1_p33_img1_two_types_of_constraints.png)`

### The Twin Peaks model (Cleland-Huang et al. 2013)
**Definition:** A model that depicts requirements and architecture as *two peaks* that are explored together: as requirements get more detailed and implementation-dependent, the architecture also gets more detailed; the two co-evolve rather than one preceding the other.
**Why it matters:** It refutes the waterfall myth that requirements come first and architecture follows. In practice, you discover architectural constraints while elaborating requirements, and vice versa.
**Detailed explanation:** The lecture presents three variants: (a) the *basic* twin peaks — two triangles, requirements on the left, architecture on the right, both growing from general/independent to detailed/dependent; (b) the *design alternatives* version — multiple candidate architectures considered against requirements; (c) the *mountain range* version — many partial peaks of requirements and many partial peaks of architecture, exchanged back and forth as the system matures. The mountain range is the realistic one.
**Analogy:** Two people building a Lego set together with no instructions — one knows what the finished thing should look like (requirements), the other knows how the blocks snap (architecture). Neither finishes their picture without conversation; every refinement on one side prompts a refinement on the other.
**Example:** The customer says "users must log in." The architect proposes OAuth. The customer responds "actually, our users have no email accounts." Now the requirement and the architecture both refine — the customer learns to articulate "identity management without email," and the architect switches from OAuth to phone-OTP. Both peaks grow taller together.
**Common pitfall / nuance:** Students draw the twin peaks once and treat it as static. The mountain range version is the key insight: you sketch and re-sketch many times, picking among design alternatives at each round, with the right-hand peaks deliberately kept *few* (two or three alternatives is enough — keep the vocabulary small for clarity).
**Related diagram:** `![Twin peaks, mountain range version](../images/lecture_1/lecture_1_p36_img1_twin_peaks_mountain_range.png)`

### The ten-term vocabulary (module, component, connector, etc.)
**Definition:** The lecture fixes a precise vocabulary of ten concepts the course will use, blended from Bass et al. and Lano & Tehrani:
1. **Module** — a large unit of code (think Java packages).
2. **Interface** — connects two or more modules.
3. **Component** — a large collection of source-code modules and other elements (servers, databases, etc.).
4. **Process** — a Unix-style OS process.
5. **Machine** — a physical or virtual machine running an OS.
6. **System** — one or more machines with components.
7. **Deployment** — a system that is running in production.
8. **Environment** — surrounding for a deployment.
9. **Element** — generic catch-all: module / component / process / machine / system / deployment.
10. **Connector** — catch-all for everything (including interfaces) with which elements talk to each other.
**Why it matters:** Every later lecture, every exam answer, will use these words with these meanings. Mixing them up loses points.
**Detailed explanation:** Two things to internalize. First, the *containment hierarchy*: code → modules → components → processes → machines → systems → deployments → environments. Second, the *no-1:1 rule*: many components can run in parallel built from the same modules; a single component may host multiple processes (a container counts as one). A "small system" might be a component with two processes inside a VM on your laptop, but the course mainly concerns large distributed systems with potentially millions of machines.
**Analogy:** A restaurant chain. *Modules* are recipes. *Components* are kitchens that combine recipes into menus. *Processes* are individual cooks executing the recipes. *Machines* are the physical buildings. *System* is the company at one moment. *Deployment* is the company actually operating in cities today. *Environment* is the economy and customer base around them. Two restaurants of the same chain use the same recipes (modules) but run as separate components.
**Example:** In the flight reservation example: "Reserve flights" and "Reserve hotel rooms" are modules; "Server" and "Client" are components; the arrows between provided and required interfaces are connectors.
**Common pitfall / nuance:** Don't expect 1:1 between modules and components. The same module can live in many components running in parallel. The course mostly operates at the **component level** because that is where most architectural reasoning happens; modules are reserved for code-level discussions.
**Related diagram:** `![Concepts illustration](../images/lecture_1/lecture_1_p40_img1_concepts_components_modules_connectors.png)`

### Component structures
**Definition:** A component structure is a description of the major executing components and how they interact. Component structures are the *key units* of an architecture for this course.
**Why it matters:** Component diagrams are what you will most often draw and reason about. The exam questions about "what are the major components, how do they communicate, where can data be replicated, where can parallel execution happen" all live here.
**Detailed explanation:** A good component should be **cohesive** (one clear responsibility), **encapsulated** (internals hidden behind interfaces), **reusable**, **substitutable**, **independently deployable**, and **composable** into larger systems. The questions a component structure helps you answer: what are the major executing units, which parts can be replicated, how does data flow, where can parallel/concurrent execution happen?
**Analogy:** Lego bricks. Each brick (component) snaps onto others via studs (provided interfaces) and accepts studs in its holes (required interfaces). You don't open a brick to use it — you just snap it in. You can swap a 2x4 for two 2x2s as long as the connection points match. You can replicate the same brick in many builds.
**Example:** In the reservation system, "Server" is a component providing flight services and hotel rooms; "Client" is a component requiring those services. Each is reusable, substitutable, and deployable on its own.
**Common pitfall / nuance:** Don't confuse "component" with "class" or "module." A component is a much bigger thing — code + data + runtime — that is built from many modules.
**Related diagram:** `![Client-server component diagram](../images/lecture_1/lecture_1_p46_img1_client_server_component_diagram.png)`

### Views and viewpoints
**Definition:** A *view* is a representation of one or more structures, chosen to highlight what some stakeholder needs to see. A *viewpoint* is the perspective/convention from which a view is built. Different views are different *representations* of the same underlying architecture.
**Why it matters:** No single diagram captures a system. Different stakeholders (developers, ops engineers, customers, security) need different views. Producing the right view for the right audience is a core architect skill.
**Detailed explanation:** Fairbanks (2010) lists view *operations*: projection (subset of details), partition (subdivide), composition (combine), classification (type→instance), generalization (supertype→subtype), designation (correspondence), refinement (low→high detail), binding (conform to pattern), dependency (one model changing forces another). The lecture also presents **Kruchten's 4+1** viewpoints: Logical (end-users, functionality), Development (developers, product owners), Process (integrators, performance, scalability), Physical (system engineers, topology), plus Scenarios in the center that tie them together.
**Analogy:** A house drawing. The floor plan (logical view) shows rooms; the electrical schematic (process view) shows wiring; the plot map (physical view) shows the lot. The architect draws all three — each is a view of the same house. The carpenter cares about one set, the electrician about another, the city inspector about a third.
**Example:** The lecture shows the reservation system in four views: full UML component diagram, a refinement, a "pseudo" simplified version, and a cloud-internet sketch. They are *designations* of each other — same system, different views.
**Common pitfall / nuance:** Students show one diagram and call it the architecture. The right move is to declare *which view* you're drawing, *which viewpoint* it uses, and *who it's for*. Note the lecturer also stresses: documentation isn't only internal — views matter when *buying and selling* software.
**Related diagrams:**
- `![Decomposition vs client-server views](../images/lecture_1/lecture_1_p52_img1_decomposition_vs_clientserver_view.png)`
- `![Synchronous vs asynchronous notations](../images/lecture_1/lecture_1_p53_img1_sync_async_notations.png)`
- `![Kruchten 4+1 viewpoints](../images/lecture_1/lecture_1_p54_img1_kruchten_4plus1_views.png)`

### The substitution principle (Liskov, generalized to components)
**Definition:** Component B can substitute for component A if (1) B preserves all of A's provided interfaces (B provides the same or more); (2) the signatures and behavior of those provided interfaces are unchanged; (3) B requires the same or fewer interfaces than A did.
**Why it matters:** Substitutability is the architectural guarantee behind upgrades, A/B testing, vendor swaps, and gradual migrations. If you cannot substitute, you cannot evolve safely.
**Detailed explanation:** This is Liskov's substitution principle (LSP) — originally about subtypes and objects — lifted to the component level by Lano & Tehrani. The intuition: the surrounding system relied on A's contract; the replacement must honor that contract entirely. B can be *richer* on what it provides (extra optional interfaces), and *leaner* on what it requires (fewer dependencies), but never the reverse. If B asks for something A never asked for, the host system isn't equipped to give it.
**Analogy:** Replacing an electrical appliance. A new toaster that uses the same plug and same voltage (provided interface preserved) and asks for nothing extra (no required interface added) is a drop-in replacement. A toaster that needs gas as well as electricity (added required interface) cannot drop into a kitchen that only has electric outlets — the surrounding system doesn't provide what the new component requires.
**Example:** The lecture walks three swaps. Component **A** (server with flight + hotel services) → Component **B** (same interfaces, internals different): valid substitute. → Component **C** (only hotel rooms — drops the flight interface): NOT a valid substitute, because the client still expects to reserve flights. → Component **D** (matches A's needs but with extra required interfaces): NOT valid, because A's host can't provide those extras.
**Common pitfall / nuance:** Students often get the *direction* wrong: "more is better." For *provided* interfaces, more is fine. For *required* interfaces, more is fatal — the host environment was designed only for A's requirements.
**Related diagrams:**
- `![Substitution principle example](../images/lecture_1/lecture_1_p56_img1_substitution_principle_example.png)`
- `![Liskov component substitution rules](../images/lecture_1/lecture_1_p60_img1_liskov_component_substitution.png)`

### Cohesion (and the vendor lock-in corollary)
**Definition:** A cohesive component does one related thing well; a non-cohesive component bundles unrelated responsibilities.
**Why it matters:** Cohesion is the first sanity check on whether you've drawn the right component boundaries. Low cohesion almost always signals an architecture problem.
**Detailed explanation:** The lecturer's running example: if the "Server" component also contains a "Marketing" module that talks to Google Ads, the server is *not* cohesive — flight reservations and ad campaigns have nothing to do with each other. Bass et al. extend this into a related rule: an architecture should never depend on a *particular vendor* and its tool versions. If a vendor dependency is unavoidable, the architecture should make swapping vendor versions cheap. That is the **no-vendor-lock-in** principle.
**Analogy:** A kitchen drawer. A cohesive drawer holds all your forks. A non-cohesive drawer holds forks, screwdrivers, batteries, and last year's tax receipts. The first is easy to reason about; the second is the source of "where did I put…" panic for years.
**Example:** Lecture slide: the "Server" has flight services, hotel rooms, AND a marketing module talking to Google. Two failures: low cohesion (marketing has no business being there) and vendor lock-in (Google specifically baked in).
**Common pitfall / nuance:** "Cohesion" is not "fewer responsibilities is always better." A *single* responsibility is the goal (see single responsibility principle). But within a single responsibility, multiple modules cooperating is fine — the test is whether they all serve the *same* clearly defined purpose.

### The segregation principle (interface segregation)
**Definition:** Components and their modules should not depend on components, connectors, or interfaces they do not actually use. Equivalently: prefer many small fine-grained interfaces over one fat one.
**Why it matters:** Unnecessary dependencies waste development effort, slow deployments, and create legal/security/licensing risk surfaces.
**Detailed explanation:** Two perspectives: (a) for *in-house* architectures, autonomous components are usually preferable — they may duplicate functionality (some bloat), but autonomy beats coupling. (b) For *suppliers* of components (libraries, services), fine-grained interfaces are preferable to a single fat interface forced on all users. A client that only wants hotel-room search should not have to depend on the entire flight-services interface.
**Analogy:** A buffet vs. a fixed menu. A buffet (fine-grained interfaces) lets each diner take exactly what they want. A fixed menu (one fat interface) forces everyone to "accept" dishes they will never touch — and the kitchen still has to prepare them. The buffet wastes less and serves more diners well.
**Example:** Lecture extends the marketing example: now the server has both a "Run ads" *required* interface (to Google) and a "Do marketing" *provided* interface that exposes the marketing module to clients. If no client actually uses "Do marketing," it's a violation of segregation — a connector with no purpose.
**Common pitfall / nuance:** Don't confuse segregation with cohesion. Cohesion is about *what's inside* a component (one purpose). Segregation is about *what the component exposes or requires* (no unused dependencies). A component can be cohesive but still over-expose, or under-expose for fine-grained use.
**Related diagram:** `![Segregation principle violation](../images/lecture_1/lecture_1_p64_img1_segregation_principle.png)`

### Single responsibility and open-closed principles (component scope)
**Definition:** (1) **Single responsibility:** each component should have only one reason to change — i.e., one well-defined responsibility. (2) **Open-closed:** components should be changed by *adding* new functionality, not by *modifying* existing functionality.
**Why it matters:** Together they keep components stable and growable. SRP minimizes "shotgun surgery" (a single feature change touching many components); OCP minimizes regression risk on existing behavior.
**Detailed explanation:** Lano & Tehrani lift these classical OO principles to the component level. SRP says: if your component changes for *two* unrelated reasons (e.g., flight-services updates AND marketing campaign tweaks), it's two components glued together; split them. OCP says: if a new feature forces you to rewrite existing code paths, you've built a closed system; you want extension points (interfaces, plugins, configuration) that let new behavior plug in without rewriting old behavior.
**Analogy:** SRP: a Swiss Army knife is convenient but bad architecture — sharpening the scissors risks bending the screwdriver. Separate tools, separate component. OCP: a power strip is "open" — plug in any device without rewiring the wall. The wall socket itself is "closed" — once installed, you don't rewire it for each new device.
**Example:** The lecture notes the reservation example is itself ill-designed: ideally the *flight* and *hotel* services should *provide* interfaces that the server *requires*, with a separate "business component" on top — splitting responsibilities cleanly so flight changes don't touch hotel logic.
**Common pitfall / nuance:** The "one reason to change" formulation is more useful than "does one thing." Two responsibilities that change together for the same business reason can sometimes live in one component; two that change for different reasons must be split, even if they look similar.

### Module structures and the data-vs-compute separation
**Definition:** A module structure partitions a system into modules — implementation units, including source code. Modules range from layers and packages down to classes, files, functions, variables. Relations are "is-a" (inheritance) and "has-a" (composition).
**Why it matters:** Module structures answer code-level questions: how are modules isolated? How do they depend on each other? Who uses whom?
**Detailed explanation:** Two key sub-ideas. First, *user module structure*: a useful abstraction asking which modules use functionality from which other modules — perfect for analyzing impact of changes. Second, Bass et al.'s wisdom: components/modules that *produce or store* data should be separate from those that *consume* data. This separation improves modifiability — adding a new ML algorithm doesn't touch the database; adding new data doesn't force algorithm rewrites; both can be upgraded incrementally.
**Analogy:** A library and its readers. The library (data side) and the reading rooms (compute side) are separate. Adding a new reader (new algorithm) doesn't require re-shelving books. Adding new books (new data) doesn't require evicting readers. Either side can be renovated independently. If you merged them — books stacked on every desk — every change to one wrecks the other.
**Example:** The lecture's naïve ensemble-learning sketch: a Data component on one side, an Algorithm component (containing Algorithm1…Algorithmn plus a Voting module) on the other, talking through interfaces. Each side can evolve independently.
**Common pitfall / nuance:** The producer/consumer separation is *also* a separation of *change frequency*: data changes on one cadence, algorithms on another. Mixing them couples cadences.
**Related diagram:** `![Ensemble learning architecture](../images/lecture_1/lecture_1_p69_img1_ensemble_learning_architecture.png)`

### Layered structures
**Definition:** A layered structure organizes modules into layers that allow only controlled, neighbor-only interaction. In a *strictly* layered system, each layer talks only to the layer immediately above or below — no jumping. Each layer is typically a single component.
**Why it matters:** Layering is the classical architectural choice for separating concerns by abstraction level. It enables independent reasoning per layer, swap-ability of any layer's implementation, and clean isolation of change.
**Detailed explanation:** Operating systems are the canonical example: hardware → device drivers → kernel (file systems, processes, I/O buffering) → system calls → userland libraries → userland programs. Each layer interacts (synchronously or asynchronously) only with its immediate neighbor. The benefits: each layer has clear responsibilities; you can upgrade one layer without touching others (e.g., swap device drivers without recompiling the kernel); abstraction levels are explicit and pedagogically clear. The lecture's manufacturing automation example layers: Sensors (L0) → PLCs (L1) → SCADA (L2) → MES (L3) → ERP (L4) — each layer corresponds to a different abstraction (physical signal → control → supervision → execution → business).
**Analogy:** A military chain of command. A private (L0) talks to their sergeant (L1), not directly to the general (L4). The sergeant talks to the lieutenant, the lieutenant to the captain, and so on. Each rank knows its neighbors. Skip-level communication breaks the system: orders get mangled, accountability is lost, the structure stops working.
**Example:** Operating system layering (Bass et al. Fig. 1.7) and manufacturing automation layering (Nagl & Westfechtel Fig. 4.4) — both shown in the lecture.
**Common pitfall / nuance:** Real layered systems sometimes allow "skip-layer" jumps for performance (relaxed layering). The lecture is talking about the *strict* form. Also: each layer might in reality run on different hardware with different OSes, with many parallel instances at the lower layers (many sensors, many PLCs) and fewer at higher ones (one ERP). Layering is conceptual, not necessarily 1-to-1 with hardware.
**Related diagrams:**
- `![Layered operating system](../images/lecture_1/lecture_1_p72_img1_layered_operating_system.png)`
- `![Layered manufacturing automation](../images/lecture_1/lecture_1_p74_img1_layered_manufacturing_automation.png)`

### System architecture vs. enterprise architecture
**Definition:** A **system architecture** is the totality of hardware, software, and humans involved in a system. An **enterprise architecture** describes an organization's processes, information flows, personnel, organizational units (departments, teams), and how they support business goals.
**Why it matters:** The two scopes have different quality attributes and different stakeholders. A system architect optimizes a deployable artifact; an enterprise architect optimizes how an organization runs. The course mostly does the former but flags the existence of the latter.
**Detailed explanation:** The manufacturing automation example straddles both — it's a system architecture (PLCs, sensors, ERP servers, networks) but its layers also map to organizational divisions (sensing teams, control teams, supervision teams, manufacturing planning, business). An enterprise architecture's central quality attribute is *alignment*: how well does the architecture support the organization's goals? Software architects are themselves part of organizations, so even when designing for other organizations they bring their own organizational context.
**Analogy:** System architecture is the design of one ship. Enterprise architecture is the design of the shipping company (routes, ports, crew rosters, maintenance schedules, financial systems). The two interact — the ship's design must fit the company's operations — but they answer different questions.
**Example:** A hospital's emergency-response system is a system architecture. The hospital's broader IT landscape (patient records, billing, supply chain, staff scheduling, regulatory reporting) is the enterprise architecture.
**Common pitfall / nuance:** Don't try to do both at once on the exam. If the question says "design a system," draw a system architecture. If it says "how does this fit the organization," widen to enterprise concerns.

### Software architect (the role)
**Definition:** A software architect is a (usually senior) software engineer responsible for making and communicating the macroscopic structural decisions of a system.
**Why it matters:** The exam will test whether you understand the *non-technical* side of the job, especially communication. The lecturer emphasizes this.
**Detailed explanation:** From Ayas et al. (2024), the most-sought architect qualities in microservices job ads (in order of importance) are: (1) articulation and transferability of knowledge, (2) stakeholder management, (3) communication / presentation / negotiation, (4) problem solving and leadership, (5) coaching and mentoring, (6) personal development. The lecturer boldfaces #1, #2, #3 as exam-relevant. Translation: the architect's job is overwhelmingly *communication*. Pure technical brilliance without articulation is the classic "ivory tower" failure mode that Bass et al. warn against. Fairbanks suggests yardsticks like "30% of working time on actual design" as guidance for how much focused design effort to budget — the rest goes to communication, documentation, and review.
**Analogy:** A film director isn't usually the best actor, the best cinematographer, or the best editor on set. Their value is in the vision and in communicating it so everyone else can do their job. Same with architects: less coding, more conversation.
**Example:** Documentation with multiple views isn't just for engineers — it lets new team members onboard, lets the business reason about cost and schedule, and lets the company sell or buy software with credible technical claims.
**Common pitfall / nuance:** Don't picture the architect as a lone code-genius. The role is structurally collaborative; the architect who refuses to talk to stakeholders is the one who builds beautiful but unusable systems. The paradox the lecturer ends with: the hardest-to-change architectural decisions are also the ones that *enable* you to reason about and manage change as the system evolves.

## Important diagrams (catalog)

- `lecture_1_p28_img1_design_arch_implementation_pyramid.png` — Three layers (design / architecture / implementation) with tensions driven by requirements, constraints, domain knowledge, and quality attributes; the central mental model of the course.
- `lecture_1_p33_img1_two_types_of_constraints.png` — Constraints entering the architecture from outside and constraints the architecture imposes on the implementation, plus the "inhibit or exhibit" framing.
- `lecture_1_p36_img1_twin_peaks_mountain_range.png` — The realistic "mountain range" version of the Twin Peaks model showing co-evolution of requirements and architecture across many small back-and-forth peaks.
- `lecture_1_p40_img1_concepts_components_modules_connectors.png` — Illustration of the ten-term vocabulary: components containing modules, connected via interfaces and connectors at the element level.
- `lecture_1_p46_img1_client_server_component_diagram.png` — The running flight-and-hotel reservation example as a UML-style component diagram with provided and required interfaces.
- `lecture_1_p52_img1_decomposition_vs_clientserver_view.png` — Two different views (decomposition view and client-server view) of the same reservation system, with synchronous and asynchronous connectors.
- `lecture_1_p53_img1_sync_async_notations.png` — Four different notational conventions for synchronous vs. asynchronous communication (Richards 2015), illustrating that "any style works as long as you're consistent."
- `lecture_1_p54_img1_kruchten_4plus1_views.png` — Kruchten's 4+1 viewpoint model: Logical, Development, Process, Physical, plus Scenarios in the center, with stakeholders labeled on each.
- `lecture_1_p56_img1_substitution_principle_example.png` — The first substitution-principle exercise: can component B (same interfaces) substitute for component A?
- `lecture_1_p60_img1_liskov_component_substitution.png` — The two formal rules for Liskov-style component substitution: required interfaces must be Liskov-substitutable for the replacement; provided interfaces must be preserved or replaced by Liskov-substitutable ones.
- `lecture_1_p64_img1_segregation_principle.png` — Server component with an extra "Do marketing" provided interface and "Run ads" required interface to Google, illustrating segregation and vendor lock-in violations.
- `lecture_1_p69_img1_ensemble_learning_architecture.png` — A minimal ensemble-learning architecture (Data component + Algorithm component with Voting) showing the producer/consumer separation between data and compute.
- `lecture_1_p72_img1_layered_operating_system.png` — A classical layered architecture: hardware → device drivers → kernel → system calls → userland libraries → userland programs.
- `lecture_1_p74_img1_layered_manufacturing_automation.png` — Five-layer manufacturing automation: Sensors → PLCs → SCADA → MES → ERP, each layer corresponding to a different abstraction (physical signal up to business).
- `lecture_1_p77_img1_healthcare_emergency_system_sketch.png` — A sketch of a healthcare emergency system architecture with three explicit tensions: 24/7/365 availability requirement, public-procurement budget constraint, and team's lack of healthcare experience.

## Exam-relevant takeaways

- **Software architecture = elements + relations + properties**, organized into multiple structures, used for *reasoning* about a system. Memorize this definition verbatim.
- **Architecture is engineering under constraints, not art.** Every decision is justified by quality attributes, requirements, and constraints — not by elegance alone.
- **Quality attributes must be prioritized.** An architecture cannot be evaluated against a flat list of "ilities"; rank them first, then judge.
- **Constraints come in two flavors:** ones that flow into the architecture (given), and ones the architecture imposes on implementation (chosen). Be ready to identify both.
- **Twin Peaks model:** requirements and architecture co-evolve via a mountain range of small alternating refinements. Pure waterfall (requirements first, then architecture) is wrong.
- **Ten-term vocabulary** — module, interface, component, process, machine, system, deployment, environment, element, connector. Know each precisely and don't mix them up.
- **Component structures answer the macro questions:** which units run, which can replicate, where parallelism lives, how data flows.
- **A view is a representation of structures, chosen for a stakeholder.** Multiple views per system are the norm. Kruchten's 4+1 (Logical, Development, Process, Physical, Scenarios) is the canonical viewpoint set.
- **Substitution rule (Liskov for components):** replacement must *preserve* provided interfaces and *not add* required interfaces. More provided is OK; more required is fatal.
- **Five component design principles to recall:** cohesion, segregation, single responsibility, open-closed, no vendor lock-in. Be able to recognize violations in a diagram.
- **Layered structures = strict neighbor-only interaction.** OS and manufacturing automation are the two canonical examples in this lecture.
- **System architecture (the artifact) vs. enterprise architecture (the organization)** — different scopes, different quality attributes, different stakeholders.
- **Architect's top three job qualities are communication-related** (articulation, stakeholder management, communication/negotiation). Pure technical skill is necessary but insufficient.

## Cross-references

- **Likely connects to a later lecture on quality attributes / tactics / patterns** — this lecture sets up the vocabulary (quality attributes, prioritization, tensions) that later lectures will turn into concrete patterns (microservices, MVC, pipe-and-filter, etc.) and tactics (caching, replication, redundancy).
- **Likely connects to a lecture on architectural evaluation** — the prioritized-quality-attributes framing here is the foundation for ATAM-style evaluation methods (Architecture Tradeoff Analysis Method).
- **Likely connects to a microservices lecture** — Ayas et al. (2024) is cited specifically about microservices architect job ads, and the segregation/single-responsibility/no-lock-in principles introduced here are the foundation of microservices.
- **Likely connects to a lecture on documentation and views** — Kruchten's 4+1, Fairbanks' view operations (projection, partition, composition, etc.), and the case for multi-view documentation set up later material on architecture documentation standards (e.g., views and beyond, arc42).
- **Likely connects to a lecture on requirements engineering / Twin Peaks** — the Cleland-Huang twin peaks material is teed up here and probably revisited.
- **Likely connects to a lecture on architectural patterns** — the layered structures discussion (OS, manufacturing) is a teaser for the broader patterns catalog: layered, client-server, pipe-and-filter, event-driven, microservices, etc.
- **Likely connects to deployment / DevOps lectures** — the distinction between system, deployment, and environment, plus the "production / 24-7-365" example, points at later lectures about deployment topology, replication, and operations.
- **Likely connects to a lecture on architecture for ML / data systems** — the producer/consumer separation and ensemble-learning sketch hint at an ML-architecture topic later.
