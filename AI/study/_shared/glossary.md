# AI Exam Prep — Shared Glossary

This file is the canonical-terminology reference for the 10-lecture AI study
package. Every Lecture Extractor (Wave 1) is expected to use the names defined
here when introducing or cross-referencing a concept, and to record any
disagreement in the "Open canonicalisation questions" section at the bottom.

Coverage convention:
- **Introduced in** = the first lecture where the term is presented with a
  definition or first-class treatment.
- **Reused in** = later lectures where the term recurs (either as a building
  block or as part of an example).
- All slide numbers refer to the PDF page numbers of the original lecture
  slide decks.
- Lecture codes: `L02 Agents`, `L03 Uninformed Search`, `L05 Local Search`,
  `L06 Adversarial Search`, `L07 CSP`, `L09a Bayesian Networks`,
  `L09b HMM`, `L10 Intro to ML`, `L11 Regression`, `L12 Clustering`.

---

## A* search

- **Definition:** Best-first informed search algorithm that expands the node minimising $f(n) = g(n) + h(n)$, where $g(n)$ is the cost-so-far from the start and $h(n)$ is the heuristic estimate of cost-to-go. With an admissible (and consistent) heuristic, A* is complete and optimal.
- **Introduced in:** L03 (slide 7 — listed as part of the informed-search objectives) — referenced but not derived in the source slides; treated as a forward reference to the textbook.
- **Reused in:** L05 (slide 4, where hill climbing is contrasted with using the "negative of a heuristic distance to the goal").
- **Alternative names seen in source:** "A-star".
- **Notation:** $f(n)$, $g(n)$, $h(n)$.

## AC-3 (arc-consistency algorithm)

- **Definition:** Classic algorithm for enforcing arc consistency across an entire CSP. It maintains a worklist of arcs, repeatedly removes inconsistent values, and re-queues affected arcs until the worklist is empty (or a domain wipes out).
- **Introduced in:** L07 (slides 46–52, "Arc consistency" pages — algorithm name is not on the slides but the propagation procedure shown is AC-3).
- **Reused in:** —
- **Alternative names seen in source:** "Arc consistency" (the slides do not use the name "AC-3" explicitly — see open questions).
- **Notation:** —

## Action

- **Definition:** A discrete choice available to an agent in a state; in search terminology, an operator that transforms a state into a successor state.
- **Introduced in:** L02 (slide 4, "perceiving... and acting upon that environment through actuators"; slide 6 defines agent function $f: \text{percept}^* \to A$).
- **Reused in:** L03 (slide 10, "Successor Function (Operator)"), L05 (state transitions in local search), L06 (move in game tree), L07 (assigning a value to a variable), L09b (hidden state transitions), L10 (action set in RL slide 5).
- **Alternative names seen in source:** "operator" (L03 slide 5, L05 example p.6, L07 slide 7).
- **Notation:** $a$, $A$ (action set).

## Adversarial search

- **Definition:** Search in environments containing other agents whose goals conflict with the searching agent's, typically modelled as a two-player zero-sum game. The standard algorithm is minimax with alpha-beta pruning.
- **Introduced in:** L06 (slide 1, title; slide 2 "Games and adversarial search").
- **Reused in:** —
- **Alternative names seen in source:** "game tree search".
- **Notation:** —

## Agent

- **Definition:** Anything that perceives its environment through sensors and acts upon that environment through actuators. Formally, an agent is the pair (architecture, agent program) that realises an agent function mapping percept sequences to actions.
- **Introduced in:** L02 (slide 4, definition; slide 6, "Agent = architecture + program").
- **Reused in:** L03 (problem-solving agent, slide 4), L05 (local-search agent), L06 (game-playing agent), L09a (probabilistic agent), L09b (HMM as agent perceptual model), L10 (learning agent).
- **Alternative names seen in source:** —
- **Notation:** —

## Agent function

- **Definition:** Mathematical function mapping every possible percept sequence to an action, $f : P^{*} \to A$. The agent function is the abstract specification of behaviour; the agent program is its concrete implementation.
- **Introduced in:** L02 (slide 6).
- **Reused in:** L02 (every agent variant builds a more compact $f$); referenced indirectly by L03 (problem-solving agent ignores percepts during plan execution).
- **Alternative names seen in source:** —
- **Notation:** $f : P^{*} \to A$.

## Agent program

- **Definition:** Concrete piece of code (running on the architecture) that produces the agent function. Distinct from the function it implements: the program is finite; the function it realises can be infinite.
- **Introduced in:** L02 (slide 6; pseudocode examples on slides 7, 28, 30).
- **Reused in:** L02 (each agent type — reflex, model-based, goal-based, utility-based — is a different agent-program template).
- **Alternative names seen in source:** —
- **Notation:** —

## Agglomerative clustering

- **Definition:** Bottom-up hierarchical clustering that starts with each data point as its own cluster and repeatedly merges the two closest clusters until either one cluster remains or a desired number $k$ of clusters is reached.
- **Introduced in:** L12 (slides 21–22, "Agglomerative Clustering Algorithm").
- **Reused in:** —
- **Alternative names seen in source:** "Bottom-up clustering" (L12 slide 7).
- **Notation:** —

## Alpha cutoff

- **Definition:** Pruning step inside alpha-beta search performed at a MIN node. If the current beta value at the MIN node drops to or below the alpha of some MAX ancestor, search below the node stops because the MAX ancestor will never let the game reach this MIN node.
- **Introduced in:** L06 (slides 22, 34 — "Discontinue search below a MIN node whose beta value ≤ alpha value of one of its MAX ancestors").
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** $\alpha$.

## Alpha-beta pruning

- **Definition:** Optimisation of minimax that maintains running bounds $\alpha$ (lower bound on MAX's value) and $\beta$ (upper bound on MIN's value) along the current path. Subtrees that cannot influence the root are pruned, giving the same minimax value as full search but in best-case $O(b^{d/2})$ time.
- **Introduced in:** L06 (slides 20–35).
- **Reused in:** —
- **Alternative names seen in source:** "alpha-beta search" (L06 slide 41).
- **Notation:** $\alpha$, $\beta$.

## Arc consistency

- **Definition:** A binary CSP constraint $X \to Y$ is arc consistent iff for every value $x$ in $D_X$ there is at least one $y$ in $D_Y$ such that $(x, y)$ satisfies the constraint. Enforcing arc consistency over a CSP iteratively prunes domain values that have no support and can detect failure earlier than forward checking.
- **Introduced in:** L07 (slides 46–53).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** $X \to Y$.

## Atomic event

- **Definition:** A complete assignment of values to every random variable in the world; equivalently, a single cell of the full joint distribution. Atomic events are mutually exclusive and collectively exhaustive.
- **Introduced in:** L09a (slide 8).
- **Reused in:** L09a (joint, marginal, conditional probability all defined over sets of atomic events).
- **Alternative names seen in source:** —
- **Notation:** —

## Autonomy (autonomous agent)

- **Definition:** Property of an agent whose behaviour is determined by its own experience rather than by built-in knowledge from its designer; it can learn, adapt, and override its designer's hard-coded rules.
- **Introduced in:** L02 (slide 13).
- **Reused in:** L02 (learning agent slide 33), L10 (RL agent is intrinsically autonomous, slide 5).
- **Alternative names seen in source:** "learning agent" (L02 slide 33).
- **Notation:** —

## Backtracking search (for CSPs)

- **Definition:** Depth-first search adapted to CSPs in which one variable at a time is assigned and the recursion backs up the moment an assignment violates a constraint. Variable-ordering (MRV, degree) and value-ordering (LCV) heuristics, plus forward checking / arc consistency, dramatically improve the basic algorithm.
- **Introduced in:** L07 (slides 18–24).
- **Reused in:** L07 (every improvement heuristic, slides 25–34, is layered on top of backtracking).
- **Alternative names seen in source:** "CSP-BACKTRACKING" (L07 slide 24).
- **Notation:** —

## Bagging (bootstrap aggregating)

- **Definition:** Ensemble method that trains many models on bootstrap (resampled-with-replacement) subsets of the training set and averages (regression) or majority-votes (classification) the predictions, reducing variance.
- **Introduced in:** L10 (slide 20 — "Ensemble Methods (Bagging - Boosting)").
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Bayes' rule

- **Definition:** Identity $P(A \mid B) = \frac{P(B \mid A)\,P(A)}{P(B)}$, allowing us to invert a conditional probability — for example, computing the diagnostic $P(\text{cavity} \mid \text{toothache})$ from the causal $P(\text{toothache} \mid \text{cavity})$.
- **Introduced in:** L09a (slides 19–24).
- **Reused in:** L09a (Naive Bayes, slide 28), L09b (noisy-channel decoding, slide 5).
- **Alternative names seen in source:** "Bayes rule".
- **Notation:** $P(A \mid B)$.

## Bayesian network

- **Definition:** A directed acyclic graph in which each node is a random variable and each edge encodes a direct probabilistic dependence; each node carries a CPT giving $P(X_i \mid \text{Parents}(X_i))$. Together with the Markov condition, the network compactly represents a full joint distribution.
- **Introduced in:** L09a (slides 35–38).
- **Reused in:** L09a (every later slide), L10 (slide 20 — "Bayesian Belief Networks" listed as a classifier).
- **Alternative names seen in source:** "belief network" (L09a slide 35).
- **Notation:** —

## Beta cutoff

- **Definition:** Pruning step inside alpha-beta search performed at a MAX node. If the current alpha value at the MAX node rises to or above the beta of some MIN ancestor, search below the node stops because the MIN ancestor will never let the game reach this MAX node.
- **Introduced in:** L06 (slide 22 — "Beta cutoff: stop search below MAX node N if alpha(N) >= beta(i)").
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** $\beta$.

## Branching factor

- **Definition:** Maximum number of successors of any node in a search tree, written $b$. Together with depth $d$ it governs the size of the search tree as $O(b^d)$.
- **Introduced in:** L03 (slide 28).
- **Reused in:** L06 (slide 7, chess branching factor $\approx 35$; slide 19), L07 (effective branching after MRV).
- **Alternative names seen in source:** —
- **Notation:** $b$.

## Breadth-first search (BFS)

- **Definition:** Uninformed search that expands the shallowest unexpanded node, implemented with a FIFO queue. Complete; optimal when all step costs are equal; time and space $O(b^d)$.
- **Introduced in:** L03 (slides 29–35).
- **Reused in:** L07 (alternative to backtracking is implicitly compared).
- **Alternative names seen in source:** —
- **Notation:** —

## Centroid (cluster centroid)

- **Definition:** Mean position of all points currently assigned to a cluster; in K-means the centroid is the cluster's geometric centre and is updated each iteration as the average of its members.
- **Introduced in:** L12 (slide 8).
- **Reused in:** L12 (slides 13–17, k-means iterations; slide 28, "Distance Between Centroids" as a hierarchical-clustering linkage).
- **Alternative names seen in source:** "center point" (L12 slide 8).
- **Notation:** $\mu_k$ (not on slides; standard textbook notation).

## Chain rule (probability)

- **Definition:** Factorisation $P(X_1, \dots, X_n) = \prod_{i=1}^{n} P(X_i \mid X_1, \dots, X_{i-1})$. In a Bayesian network, the parents of $X_i$ d-separate it from its earlier non-descendants, reducing the chain rule to $P(X_1, \dots, X_n) = \prod_i P(X_i \mid \text{Parents}(X_i))$.
- **Introduced in:** L09a (slide 19; reused on slide 42 to derive the BN joint-distribution formula).
- **Reused in:** L09b (HMM forward derivation, slide 9).
- **Alternative names seen in source:** "product rule" (L09a slide 20).
- **Notation:** —

## Chromosome (genetic algorithm)

- **Definition:** Encoded representation of a candidate solution in a genetic algorithm, classically a fixed-length bitstring. Each chromosome is scored by the fitness function and combined with others via crossover and mutation to produce offspring.
- **Introduced in:** L05 (slides 22, 27, 31).
- **Reused in:** L05 (selection, crossover, mutation all operate on chromosomes; slides 40–48).
- **Alternative names seen in source:** "genotype", "bitstring" (L05 slides 22, 27, 31).
- **Notation:** —

## Classification

- **Definition:** Supervised-learning task in which the model maps an input feature vector to one of a finite set of discrete class labels; contrasted with regression, which predicts a continuous value.
- **Introduced in:** L10 (slides 10, 17–19).
- **Reused in:** L10 (decision trees, slides 21–60), L11 (regression is the continuous counterpart).
- **Alternative names seen in source:** —
- **Notation:** —

## Clustering

- **Definition:** Unsupervised-learning task of grouping data points so that intra-cluster distance is minimised and inter-cluster distance is maximised. Output is a partition (k-means), nesting (hierarchical), or density-based set (DBSCAN) of clusters.
- **Introduced in:** L10 (slide 4 — listed as an unsupervised-learning task).
- **Reused in:** L12 (entire lecture).
- **Alternative names seen in source:** "cluster analysis" (L12 slide 1).
- **Notation:** —

## Completeness (of a search algorithm)

- **Definition:** Property that the algorithm is guaranteed to find a solution whenever one exists (and to report failure when none does).
- **Introduced in:** L03 (slide 27).
- **Reused in:** L05 (hill climbing is not complete — slide 14; simulated annealing converges in the limit — slide 20), L06 (minimax is complete on finite game trees), L07 (backtracking is complete on finite CSPs).
- **Alternative names seen in source:** —
- **Notation:** —

## Conditional independence

- **Definition:** Two random variables $X$ and $Y$ are conditionally independent given $Z$ iff $P(X, Y \mid Z) = P(X \mid Z)\,P(Y \mid Z)$, equivalently $P(X \mid Y, Z) = P(X \mid Z)$. Conditional independence is the structural assumption that lets Bayesian networks factor the joint distribution.
- **Introduced in:** L09a (slides 39–41).
- **Reused in:** L09a (Markov condition, slides 49–54), L09b (Markov assumption, slide 10), L10 (Naive Bayes assumes attribute independence given the class, slide 28).
- **Alternative names seen in source:** —
- **Notation:** $X \perp Y \mid Z$ (L09a slide 41).

## Conditional probability

- **Definition:** Probability of event $A$ given that event $B$ has occurred, defined as $P(A \mid B) = P(A \cap B) / P(B)$ when $P(B) > 0$.
- **Introduced in:** L09a (slides 14–17).
- **Reused in:** L09a (Bayes' rule, CPTs, BN inference), L09b (HMM transition and emission probabilities).
- **Alternative names seen in source:** —
- **Notation:** $P(A \mid B)$.

## Conditional probability table (CPT)

- **Definition:** Table attached to a Bayesian-network node $X_i$ that lists $P(X_i \mid \text{Parents}(X_i))$ for every combination of parent values. A node with $k$ Boolean parents has $2^{k+1}$ entries (or $2^k$ independent entries given that each row sums to 1).
- **Introduced in:** L09a (slides 37–38).
- **Reused in:** L09a (every later example uses CPTs, slides 45–60).
- **Alternative names seen in source:** "conditional probability distribution" (L09a slide 37).
- **Notation:** —

## Consistent assignment (CSP)

- **Definition:** Partial assignment of values to variables that violates no constraint of the CSP. A *solution* is a complete consistent assignment.
- **Introduced in:** L07 (slide 6).
- **Reused in:** L07 (every backtracking-and-propagation step preserves consistency).
- **Alternative names seen in source:** —
- **Notation:** —

## Constraint (CSP)

- **Definition:** A specification that restricts which combinations of values are allowed for a subset of CSP variables; can be unary (one variable), binary (two), or global (many).
- **Introduced in:** L07 (slide 6).
- **Reused in:** L07 (slides 8–14, examples; slide 25 onward for propagation).
- **Alternative names seen in source:** —
- **Notation:** $C_1, C_2, \dots, C_m$.

## Constraint graph

- **Definition:** Graph whose nodes are CSP variables and whose edges connect variables that appear together in a constraint. Used by AC-3 and by variable-ordering heuristics such as MRV and degree.
- **Introduced in:** L07 (slide 10).
- **Reused in:** L07 (visualisation of arc consistency, slides 46–52).
- **Alternative names seen in source:** —
- **Notation:** —

## Constraint propagation

- **Definition:** Family of techniques that locally enforce constraint consistency (e.g. arc consistency) to prune domains before or during backtracking, detecting impossibilities sooner.
- **Introduced in:** L07 (slide 45).
- **Reused in:** L07 (arc consistency, slides 46–53).
- **Alternative names seen in source:** —
- **Notation:** —

## Constraint Satisfaction Problem (CSP)

- **Definition:** A triple $\langle X, D, C \rangle$ of variables $X_1, \dots, X_n$, domains $D_1, \dots, D_n$, and constraints $C_1, \dots, C_m$. A solution is a complete assignment of values from each $D_i$ to $X_i$ that satisfies every constraint.
- **Introduced in:** L07 (slides 1–6).
- **Reused in:** L07 (every later slide); L09a (random variables are "just like CSP variables" — slide 5).
- **Alternative names seen in source:** "CSP" (lecture title abbreviation).
- **Notation:** —

## Crossover (genetic algorithm)

- **Definition:** Recombination operator that combines two parent chromosomes — typically by choosing a random cut point and swapping the suffixes — to produce two offspring. Applied with probability *crossover rate* (typical 0.8–0.95).
- **Introduced in:** L05 (slides 38–43).
- **Reused in:** L05 (algorithm template, slide 45).
- **Alternative names seen in source:** "recombination" (L05 slide 43).
- **Notation:** —

## d-separation

- **Definition:** Graphical criterion on a Bayesian network that determines whether two sets of variables are conditionally independent given a third set. If every undirected path between them is "blocked" by the evidence set, they are d-separated and hence conditionally independent.
- **Introduced in:** L09a (slide 39 — "Markov condition" framing; full d-separation rules are referenced rather than fully derived on the slides).
- **Reused in:** —
- **Alternative names seen in source:** "Markov condition" (L09a slide 39).
- **Notation:** —

## DBSCAN

- **Definition:** Density-based clustering algorithm that labels each point as core (≥ MinPts neighbours within radius Eps), border (within Eps of a core point but with fewer than MinPts neighbours), or noise (neither). Clusters are maximal sets of density-connected core points; border points join the cluster of their closest core point; noise is discarded.
- **Introduced in:** L12 (slides 35–43).
- **Reused in:** —
- **Alternative names seen in source:** "Density-Based Clustering" (L12 slide 35).
- **Notation:** —

## Decision tree

- **Definition:** Tree-structured classifier (or regressor) in which each internal node tests an attribute, each branch corresponds to a value or range of that attribute, and each leaf carries a class label (or numeric prediction). Built top-down by recursively choosing the attribute that maximises a purity measure (Gini, entropy, classification error).
- **Introduced in:** L10 (slides 21–34).
- **Reused in:** L10 (slides 35–60 cover splitting, impurity, stopping criteria, overfitting).
- **Alternative names seen in source:** —
- **Notation:** —

## Degree heuristic

- **Definition:** CSP variable-ordering rule that, among the variables tied under MRV, selects the variable participating in the largest number of constraints on yet-unassigned variables.
- **Introduced in:** L07 (slide 27 — "Most constraining variable").
- **Reused in:** —
- **Alternative names seen in source:** "most constraining variable" (L07 slide 27).
- **Notation:** —

## Dendrogram

- **Definition:** Tree-shaped diagram that records the sequence of merges (agglomerative) or splits (divisive) made by a hierarchical clustering algorithm. Cutting the dendrogram horizontally at a chosen height yields a flat clustering with the corresponding number of clusters.
- **Introduced in:** L12 (slide 6; example on slide 23).
- **Reused in:** L12 (slides 20, 23).
- **Alternative names seen in source:** "Dendogram" (typo in source slides).
- **Notation:** —

## Depth-first search (DFS)

- **Definition:** Uninformed search that expands the deepest unexpanded node, implemented with a LIFO stack. Not complete in infinite-depth or cyclic graphs (without an explored set); not optimal; time $O(b^m)$ but only $O(b m)$ space — its main advantage.
- **Introduced in:** L03 (slides 38–47).
- **Reused in:** L07 (backtracking search is "DFS with single-variable assignments", slide 18), L06 (alpha-beta proceeds in DFS order, slide 22).
- **Alternative names seen in source:** —
- **Notation:** —

## Deterministic vs stochastic (environment property)

- **Definition:** An environment is deterministic if its next state is completely determined by the current state and the agent's action; otherwise it is stochastic.
- **Introduced in:** L02 (slide 18).
- **Reused in:** L02 (slides 23–24 examples), L06 (slide 5 — game environment classification), L10 (RL is described as inherently stochastic, slide 7).
- **Alternative names seen in source:** —
- **Notation:** —

## Discrete vs continuous (environment property)

- **Definition:** An environment is discrete if it provides a fixed (countable) number of distinct percepts, actions, and states; continuous environments take values from a continuum (e.g. real-valued sensor readings).
- **Introduced in:** L02 (slide 21).
- **Reused in:** L02 (slides 23–24 examples), L10 (regression is the continuous-output learning task, slide 10).
- **Alternative names seen in source:** —
- **Notation:** —

## Dummy variable

- **Definition:** Binary $\{0, 1\}$ recoding of a categorical attribute used so that a numeric regression model can incorporate categorical information. The "baseline" category receives value 0 and its effect is absorbed by the intercept; other categories' coefficients measure deviation from that baseline.
- **Introduced in:** L11 (slides 33–37).
- **Reused in:** L11 (slides 38–46, interaction terms multiply dummies with continuous features).
- **Alternative names seen in source:** "binary variable" (L11 slide 33).
- **Notation:** —

## Elitism (genetic algorithm)

- **Definition:** Selection variant in which the best-fitness chromosome(s) of a generation are copied unchanged into the next generation, guaranteeing that the best-so-far solution never deteriorates.
- **Introduced in:** L05 (slide 46 — listed as a selection variant).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Emission model (observation model, HMM)

- **Definition:** Distribution $b_k(o) = P(o \mid q = k)$ giving the probability of emitting observation $o$ while the HMM is in hidden state $k$. Together with the transition model and the initial distribution it fully parameterises an HMM.
- **Introduced in:** L09b (slide 2 — "Evidence observation model"; slide 23 — matrix $B$).
- **Reused in:** L09b (forward and Viterbi recursions, slides 36–48).
- **Alternative names seen in source:** "observation model", "emission probabilities" (L09b slide 24).
- **Notation:** $b_k(o)$, matrix $B$.

## Ensemble method

- **Definition:** Classifier (or regressor) built by combining the outputs of many base learners — by majority vote (classification) or averaging (regression). Common ensembles: bagging, boosting, random forest.
- **Introduced in:** L10 (slide 20).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Entropy (information-theoretic, splitting criterion)

- **Definition:** Measure of class-impurity at a decision-tree node: $\text{Entropy}(t) = -\sum_j p(j \mid t) \log_2 p(j \mid t)$. Maximised when classes are perfectly mixed; zero when the node is pure. Used as the splitting criterion in ID3/C4.5 via information gain.
- **Introduced in:** L10 (slides 48–49).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** $\text{Entropy}(t)$.

## Environment (task environment)

- **Definition:** Everything outside the agent — the world the agent perceives via sensors and acts on via actuators. Specified in PEAS form by performance measure, environment, actuators, sensors.
- **Introduced in:** L02 (slide 4; slide 14 PEAS).
- **Reused in:** L02 (every example), L06 (competitive multi-agent environment, slide 3), L09b (partially-observable environment with hidden state).
- **Alternative names seen in source:** —
- **Notation:** —

## Environment types (taxonomy)

- **Definition:** Six binary properties used to classify task environments: fully vs partially observable, deterministic vs stochastic, episodic vs sequential, static vs dynamic, discrete vs continuous, single- vs multi-agent.
- **Introduced in:** L02 (slides 16–24).
- **Reused in:** L06 (slide 5 — game-environment classification overlay), L09a (introduces uncertainty as a consequence of partial observability + stochasticity, slide 2).
- **Alternative names seen in source:** —
- **Notation:** —

## Episodic vs sequential (environment property)

- **Definition:** Episodic environments split experience into independent episodes; the choice of action in one episode does not affect future episodes. Sequential environments require reasoning about the long-term consequences of an action.
- **Introduced in:** L02 (slide 19).
- **Reused in:** L02 (slides 23–24 examples).
- **Alternative names seen in source:** —
- **Notation:** —

## Evaluation function

- **Definition:** Heuristic estimate of the utility of a non-terminal game state, used when game trees are too deep to search to terminal nodes. For Tic-Tac-Toe the slides use *X's open lines − O's open lines*.
- **Introduced in:** L06 (slide 30 — "Utility = X's open lines − O's open lines"; slide 41 attributes the idea to Shannon 1949).
- **Reused in:** L06 (every depth-limited example).
- **Alternative names seen in source:** "utility function" (L02 slide 32 — utility-based agent context); the two terms are used interchangeably across L02 and L06.
- **Notation:** —

## Evidence (Bayesian inference)

- **Definition:** Observed values of one or more variables that we condition on when computing a query. In a Bayes-net inference $P(X \mid E)$, $E$ denotes the evidence variables and their observed values.
- **Introduced in:** L09a (slide 43).
- **Reused in:** L09b (the observation sequence plays the role of evidence in HMM filtering and decoding).
- **Alternative names seen in source:** —
- **Notation:** $E$.

## Expected utility

- **Definition:** Probability-weighted average of the utilities of all outcomes of an action: $\sum_i P(\text{outcome}_i \mid \text{action})\,U(\text{outcome}_i)$. A rational agent chooses the action that maximises expected utility.
- **Introduced in:** L09a (slide 3 — airport-arrival example).
- **Reused in:** L02 (slide 37 — rational agent maximises expected performance).
- **Alternative names seen in source:** —
- **Notation:** $\mathbb{E}[U]$.

## Filtering (HMM problem 1)

- **Definition:** Computing $P(O \mid \lambda)$ — the likelihood of the observation sequence $o_1, \dots, o_T$ given the model $\lambda = (A, B, \pi)$. Solved efficiently by the forward algorithm in $O(N^2 T)$ time.
- **Introduced in:** L09b (slide 29 — "Problem 1 (Evaluation)").
- **Reused in:** L09b (forward algorithm, slides 35–41).
- **Alternative names seen in source:** "Evaluation problem" (L09b slide 29 — slides do not use the name "filtering" explicitly; see open questions).
- **Notation:** $P(O \mid \lambda)$.

## Fitness function

- **Definition:** Real-valued function that scores how good a candidate solution (chromosome) is for the problem at hand; the genetic algorithm preferentially selects high-fitness individuals for reproduction.
- **Introduced in:** L05 (slides 22, 33, 40).
- **Reused in:** L05 (every later slide).
- **Alternative names seen in source:** "score" (L05 slide 27).
- **Notation:** —

## Forward algorithm (HMM)

- **Definition:** Dynamic-programming algorithm that computes $P(o_1, \dots, o_T \mid \lambda)$ by filling a trellis $\alpha_t(j) = P(o_1, \dots, o_t, q_t = j \mid \lambda)$. Runs in $O(N^2 T)$ instead of the brute-force $O(N^T)$.
- **Introduced in:** L09b (slides 35–41).
- **Reused in:** L09b (Viterbi uses an analogous trellis but with $\max$ instead of $\sum$, slides 45–51).
- **Alternative names seen in source:** —
- **Notation:** $\alpha_t(j)$.

## Forward checking

- **Definition:** Lightweight constraint-propagation rule applied after each variable assignment: remove from every unassigned neighbour's domain the values that are now inconsistent. If any domain becomes empty, backtrack immediately.
- **Introduced in:** L07 (slides 30–34).
- **Reused in:** L07 (precursor to arc consistency, slide 45).
- **Alternative names seen in source:** —
- **Notation:** —

## Frequentism

- **Definition:** Interpretation of probability as the long-run relative frequency of an event over many independent trials.
- **Introduced in:** L09a (slide 4).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Frontier (search)

- **Definition:** Set of nodes that have been generated by the search but not yet expanded; the data structure (FIFO queue, LIFO stack, priority queue) used for the frontier determines which uninformed strategy results (BFS, DFS, UCS respectively).
- **Introduced in:** L03 (slide 20 — "Maintain a fringe or a list of unexpanded states").
- **Reused in:** L03 (every algorithm uses the frontier), L07 (backtracking implicitly).
- **Alternative names seen in source:** "fringe" (L03 slide 20).
- **Notation:** —

## Fully observable vs partially observable (environment)

- **Definition:** An environment is fully observable when the agent's sensors give it access to the complete state at every time step; partially observable when some aspects of the world state are hidden.
- **Introduced in:** L02 (slide 17).
- **Reused in:** L02 (model-based reflex agent is the answer to partial observability, slide 29), L06 (slide 5 — perfect-information vs imperfect-information games), L09b (HMM is the canonical partially observable model, slide 2).
- **Alternative names seen in source:** —
- **Notation:** —

## Genetic algorithm (GA)

- **Definition:** Population-based stochastic optimisation inspired by Darwinian evolution. Maintains a population of chromosomes, scores them with a fitness function, and iterates selection → crossover → mutation to evolve high-fitness individuals.
- **Introduced in:** L05 (slides 21–48).
- **Reused in:** —
- **Alternative names seen in source:** "GA" (L05 slide 21).
- **Notation:** —

## Gini impurity

- **Definition:** Class-impurity measure used in CART / SLIQ / SPRINT: $\text{Gini}(t) = 1 - \sum_j p(j \mid t)^2$. Zero when all records at the node share one class; maximum $1 - 1/n_c$ when classes are evenly mixed across $n_c$ classes.
- **Introduced in:** L10 (slides 42–47).
- **Reused in:** L10 (slide 52, comparison among splitting criteria).
- **Alternative names seen in source:** "Gini Index" (L10 slide 42).
- **Notation:** $\text{Gini}(t)$.

## Goal-based agent

- **Definition:** Agent that maintains explicit knowledge of one or more goal states and chooses actions whose predicted consequences move the agent closer to a goal.
- **Introduced in:** L02 (slide 31).
- **Reused in:** L03 (problem-solving agent is a special case of goal-based agent, slide 8).
- **Alternative names seen in source:** —
- **Notation:** —

## Goal state

- **Definition:** The state (or one of a set of states) that the agent is trying to reach; the goal test returns *true* exactly on goal states.
- **Introduced in:** L03 (slide 10).
- **Reused in:** L03 (every example), L05 (local search drops the notion of an explicit goal in favour of an objective function, slide 2), L07 (CSP goal is a complete consistent assignment, slide 7).
- **Alternative names seen in source:** —
- **Notation:** —

## Hidden Markov Model (HMM)

- **Definition:** A statistical sequence model with a hidden discrete-state Markov chain and an observable emission process. Parameterised by $\lambda = (A, B, \pi)$: transition matrix, emission matrix, initial-state distribution. Used for speech, POS tagging, and any task where evidence is observed but the underlying state is not.
- **Introduced in:** L09b (slides 1, 16–24).
- **Reused in:** —
- **Alternative names seen in source:** "HMM".
- **Notation:** $\lambda = (A, B, \pi)$.

## Hidden state

- **Definition:** A latent (unobserved) state of the HMM that the algorithm must infer from the observation sequence; in the ice-cream example the hidden state is the weather, in the casino example the coin.
- **Introduced in:** L09b (slides 16, 22).
- **Reused in:** L09b (every later slide).
- **Alternative names seen in source:** —
- **Notation:** $q_t$.

## Hierarchical clustering

- **Definition:** Clustering technique that produces a tree of nested clusterings rather than a single flat partition; can be agglomerative (bottom-up) or divisive (top-down). A flat clustering of any desired number of clusters is obtained by cutting the dendrogram.
- **Introduced in:** L12 (slides 4, 6, 20–34).
- **Reused in:** L12 (Ward's method ties hierarchical to K-means, slide 33).
- **Alternative names seen in source:** —
- **Notation:** —

## Heuristic function

- **Definition:** Domain-specific estimate $h(n)$ of the cost from node $n$ to the nearest goal. In informed search it guides node expansion (greedy, A*); in local search it directly drives the objective (hill climbing uses $-h$).
- **Introduced in:** L05 (slide 4 — "negative of a heuristic distance to the goal"; the term is also forward-referenced in L03 slide 7).
- **Reused in:** L05 (n-queens heuristic $h = 17$, slide 10; 8-puzzle $h = -\text{tiles out of place}$, slide 5), L06 (evaluation function is a heuristic for game-tree leaves).
- **Alternative names seen in source:** "heuristic cost estimate" (L05 slide 11).
- **Notation:** $h(n)$.

## Hill climbing

- **Definition:** Local-search algorithm that, at each step, moves to the best-valued neighbour of the current state and terminates when no neighbour improves on the current value. Greedy: simple and memory-light but easily trapped in local maxima, plateaux, and ridges.
- **Introduced in:** L05 (slides 4–14).
- **Reused in:** L05 (random-restart variant, slide 15; comparison with simulated annealing, slides 16–17).
- **Alternative names seen in source:** "greedy search" (L05 slide 4).
- **Notation:** —

## Independence

- **Definition:** Two events $A$ and $B$ are independent iff $P(A \cap B) = P(A)\,P(B)$, equivalently $P(A \mid B) = P(A)$. A key simplifying assumption that allows a joint distribution to be factored.
- **Introduced in:** L09a (slide 25).
- **Reused in:** L09a (Naive Bayes assumption, slide 28; conditional independence generalisation, slide 39).
- **Alternative names seen in source:** —
- **Notation:** $A \perp B$.

## Inference by enumeration

- **Definition:** Exact-inference algorithm for Bayesian networks that computes a query $P(X \mid e)$ by summing the joint distribution over all atomic events consistent with the evidence and renormalising. Correct but exponential in the number of unobserved variables.
- **Introduced in:** L09a (slides 43–62, particularly slide 61 — "joint entry $E_1 E_2$ matching... ").
- **Reused in:** —
- **Alternative names seen in source:** "exact inference" (L09a slide 64).
- **Notation:** —

## Information gain

- **Definition:** Reduction in entropy achieved by splitting a decision-tree node on a particular attribute: $\text{IG} = \text{Entropy}(\text{parent}) - \sum_i \frac{n_i}{n} \text{Entropy}(\text{child}_i)$. ID3 / C4.5 choose the split with the largest information gain.
- **Introduced in:** L10 (slide 48 — entropy; slide 59 — "improve impurity measures (e.g., Gini or information gain)").
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** $\text{IG}$.

## Initial distribution (HMM)

- **Definition:** Probability vector $\pi_i = P(q_1 = i)$ specifying the probability that the HMM starts in each hidden state.
- **Introduced in:** L09b (slide 11).
- **Reused in:** L09b (forward initialisation, slide 37; Viterbi initialisation, slide 48).
- **Alternative names seen in source:** "initial probability vector", "priors" (L09b slide 2).
- **Notation:** $\pi$.

## Initial state

- **Definition:** The state the agent is in when search begins (or the assignment from which CSP backtracking starts — the empty assignment).
- **Introduced in:** L03 (slide 10).
- **Reused in:** L03 (every example), L07 (slide 7 — empty assignment), L09b (initial distribution).
- **Alternative names seen in source:** —
- **Notation:** —

## Interaction term

- **Definition:** In a regression model, a feature formed as the product of two existing features (often a dummy and a continuous variable). Including it allows the model to express different slopes for different categories — non-parallel regression lines.
- **Introduced in:** L11 (slides 26–28, 41–46).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Intercept (regression)

- **Definition:** Constant term $a$ in a linear-regression equation $y = a + b x$; the predicted response when every predictor is zero, and the baseline value when dummy variables are 0.
- **Introduced in:** L11 (slides 7, 11, 37).
- **Reused in:** L11 (every regression equation).
- **Alternative names seen in source:** —
- **Notation:** $a$.

## Iterative deepening search (IDS)

- **Definition:** Uninformed strategy that runs depth-limited DFS for depth 0, 1, 2, … until a goal is found. Combines the linear-space advantage of DFS with the completeness and optimality (unit-cost) of BFS, at $O(b^d)$ time.
- **Introduced in:** L03 (slides 48–53).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Joint probability distribution

- **Definition:** Assignment of a probability to every atomic event of the world; equivalently, a probability table over the Cartesian product of all variables' domains. For $n$ binary variables it has $2^n$ entries.
- **Introduced in:** L09a (slides 9–10).
- **Reused in:** L09a (marginalisation, conditional probability, BN factorisation, slides 11–18, 42).
- **Alternative names seen in source:** "full joint" (textbook); on the slides simply "joint distribution".
- **Notation:** $P(X_1, \dots, X_n)$.

## K-means clustering

- **Definition:** Partitional clustering algorithm. Given $K$, repeatedly (1) assign each point to the nearest centroid, (2) recompute each centroid as the mean of its assigned points, until centroids stop moving. Locally minimises the within-cluster sum-of-squares (inertia).
- **Introduced in:** L12 (slides 7–17).
- **Reused in:** L12 (Ward's method is the hierarchical analogue, slide 33).
- **Alternative names seen in source:** —
- **Notation:** $K$.

## Learning agent

- **Definition:** Agent containing a learning element that improves the performance element from experience, a critic that judges performance, and a problem generator that proposes exploratory actions. Generalisation of the autonomous agent.
- **Introduced in:** L02 (slides 33–35).
- **Reused in:** L10 (the entire ML lecture is about how to build the learning element).
- **Alternative names seen in source:** "Autonomous agent" (L02 slide 33).
- **Notation:** —

## Least Constraining Value (LCV)

- **Definition:** CSP value-ordering rule that, when assigning a chosen variable, tries the value that removes the fewest values from the domains of remaining unassigned variables.
- **Introduced in:** L07 (slides 28–29).
- **Reused in:** —
- **Alternative names seen in source:** "Least constraining value heuristic".
- **Notation:** —

## Linear regression

- **Definition:** Supervised-learning model that fits a linear equation $y = a + b_1 x_1 + \dots + b_p x_p$ to data by minimising the sum of squared residuals (ordinary least squares). The simplest predictive model and the foundation for more flexible variants.
- **Introduced in:** L11 (slides 1–11).
- **Reused in:** L11 (every later slide extends or interprets it).
- **Alternative names seen in source:** "Least Squares Regression" (L11 slide 10).
- **Notation:** $y = a + b x$.

## Local maximum

- **Definition:** State whose objective-function value is higher than that of every neighbour but lower than the global maximum. Hill climbing terminates at a local maximum; simulated annealing and random restarts are designed to escape them.
- **Introduced in:** L05 (slide 14).
- **Reused in:** L05 (motivates simulated annealing, slide 16; "Fitness landscapes" — slide 35).
- **Alternative names seen in source:** "local optima" (L05 slide 14).
- **Notation:** —

## Local search

- **Definition:** Family of search techniques that keep one (or a few) current states and iteratively modify them, ignoring the path to a solution. Used for optimisation problems where only the goal — not the route — matters.
- **Introduced in:** L05 (slides 1–2).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Marginal probability distribution

- **Definition:** Distribution of a subset of variables obtained from the joint by summing (or integrating) over the others: $P(X) = \sum_y P(X, Y = y)$.
- **Introduced in:** L09a (slides 11–13).
- **Reused in:** L09a (inference by enumeration).
- **Alternative names seen in source:** —
- **Notation:** —

## Markov assumption (first-order)

- **Definition:** The conditional independence assumption $P(q_t \mid q_1, \dots, q_{t-1}) = P(q_t \mid q_{t-1})$: the current state depends only on the immediately previous one.
- **Introduced in:** L09b (slide 10).
- **Reused in:** L09b (every HMM derivation), L09a (Markov condition is the analogous structural assumption for Bayes nets, slide 39).
- **Alternative names seen in source:** "Markov property".
- **Notation:** —

## Markov chain

- **Definition:** Probabilistic model defined by a finite set of states, a transition probability matrix $A$ with $a_{ij} = P(q_t = j \mid q_{t-1} = i)$, and an initial distribution. In a Markov chain the states are observable; an HMM is its hidden-state extension.
- **Introduced in:** L09b (slides 6–14).
- **Reused in:** L09b (every HMM concept is layered on top).
- **Alternative names seen in source:** "first-order observable Markov model" (L09b slide 9).
- **Notation:** $A$.

## Markov condition (for Bayes nets)

- **Definition:** A node in a Bayesian network is conditionally independent of all its non-descendants given its parents. This is the structural assumption that lets the chain rule collapse to the BN factorisation $P(X_1, \dots, X_n) = \prod_i P(X_i \mid \text{Parents}(X_i))$.
- **Introduced in:** L09a (slides 39–42).
- **Reused in:** L09a (every BN inference derivation).
- **Alternative names seen in source:** "Conditional independence in Bayes nets".
- **Notation:** —

## Minimax

- **Definition:** Two-player zero-sum game algorithm. At MAX nodes choose the move with the highest minimax value of successor states; at MIN nodes choose the lowest. Recurses to terminal nodes (or to an evaluation function at a depth limit). Optimal against an optimal opponent.
- **Introduced in:** L06 (slides 11–15).
- **Reused in:** L06 (alpha-beta is an exact optimisation of minimax, slides 20–35).
- **Alternative names seen in source:** "Minmax" (L06 slide 11).
- **Notation:** $\text{Minimax}(s)$.

## Minimum Remaining Values (MRV)

- **Definition:** CSP variable-ordering rule that always picks next the unassigned variable with the smallest current legal domain — the "most-constrained variable" heuristic, designed to fail fast.
- **Introduced in:** L07 (slide 26).
- **Reused in:** —
- **Alternative names seen in source:** "most constrained variable" (L07 slide 26).
- **Notation:** —

## Model-based reflex agent

- **Definition:** Agent that maintains an internal state estimating aspects of the world its sensors cannot directly observe, using a transition model that says how the world evolves given actions. Designed for partially observable environments.
- **Introduced in:** L02 (slides 29–30).
- **Reused in:** L09b (HMM-based agents are the probabilistic analogue).
- **Alternative names seen in source:** "Agent with memory" / "Agent with state" (L02 slide 25).
- **Notation:** —

## Multicollinearity

- **Definition:** Situation in which two or more regression predictors are strongly correlated, making their individual coefficients unstable and hard to interpret. Diagnosed via correlation tables and scatterplots; "cured" by careful variable selection.
- **Introduced in:** L11 (slides 47–48).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Multi-agent (environment property)

- **Definition:** An environment is multi-agent when the agent must take into account the actions of other agents that affect its performance — competitive or cooperative.
- **Introduced in:** L02 (slide 22).
- **Reused in:** L06 (slide 3 — competitive multi-agent), L10 (RL with self-play is implicitly multi-agent, slide 6).
- **Alternative names seen in source:** —
- **Notation:** —

## Mutation (genetic algorithm)

- **Definition:** Operator that with small probability (the mutation rate, typically 0.001–0.1) flips a random gene of an offspring chromosome, injecting exploration into the population and preventing premature convergence.
- **Introduced in:** L05 (slide 44).
- **Reused in:** L05 (algorithm template, slide 45).
- **Alternative names seen in source:** —
- **Notation:** —

## Naive Bayes classifier

- **Definition:** Probabilistic classifier that assumes the features are conditionally independent given the class: $P(A_1, \dots, A_n \mid C) = \prod_i P(A_i \mid C)$. The class chosen is $\arg\max_C P(C) \prod_i P(A_i \mid C)$.
- **Introduced in:** L09a (slides 27–29).
- **Reused in:** L10 (slide 20 — "Probabilistic Methods (Naive Bayes and Bayesian Belief Networks)").
- **Alternative names seen in source:** —
- **Notation:** —

## Node (search tree)

- **Definition:** Data structure in a search tree representing one path-end during the search; carries the underlying state plus bookkeeping (parent pointer, action taken, path cost, depth). Distinct from "state": multiple nodes may share a state.
- **Introduced in:** L03 (slide 20 — "Nodes vs. states").
- **Reused in:** L03, L06 (game-tree nodes), L07 (backtracking nodes).
- **Alternative names seen in source:** —
- **Notation:** $n$.

## Objective function

- **Definition:** Real-valued function whose maximum (or minimum) defines the goal of an optimisation problem. In local search the agent has no explicit goal state — only an objective to climb.
- **Introduced in:** L05 (slide 2).
- **Reused in:** L05 (every algorithm), L11 (the OLS objective is the sum of squared residuals).
- **Alternative names seen in source:** "value function".
- **Notation:** —

## Observation (HMM)

- **Definition:** Symbol emitted by the HMM at a time step; observations are the only information available to the inference algorithm — the underlying state remains hidden.
- **Introduced in:** L09b (slides 22, 27).
- **Reused in:** L09b (every later slide).
- **Alternative names seen in source:** "emission" (L09b slide 22), "evidence" (L09b slide 2).
- **Notation:** $o_t$.

## Optimality (of a search algorithm)

- **Definition:** Property that the algorithm is guaranteed to return a *least-cost* solution whenever a solution exists.
- **Introduced in:** L03 (slide 27).
- **Reused in:** L03 (UCS is optimal, BFS is optimal only when step costs are equal, DFS is not optimal), L05 (hill climbing is not optimal), L06 (minimax is optimal vs an optimal opponent).
- **Alternative names seen in source:** —
- **Notation:** —

## Ordinary Least Squares (OLS)

- **Definition:** Estimation procedure that picks the regression coefficients minimising $\sum_i (y_i - \hat{y}_i)^2$ — the sum of squared residuals.
- **Introduced in:** L11 (slide 10 — "Least squares regression... minimizes the sum of all squared residuals").
- **Reused in:** —
- **Alternative names seen in source:** "Least squares regression" (L11 slide 10).
- **Notation:** —

## Overfitting

- **Definition:** Phenomenon where a model fits the training data — including its noise — too closely and therefore generalises poorly to unseen data. Diagnosed by training error decreasing while test error increases; cured by pruning, simpler models, more data, regularisation.
- **Introduced in:** L10 (slides 55–60).
- **Reused in:** L11 (motivates careful variable selection / multicollinearity, slides 47–48).
- **Alternative names seen in source:** —
- **Notation:** —

## p-value (regression coefficient)

- **Definition:** Probability of observing a coefficient at least as extreme as the estimated one if the true coefficient were zero. A small p-value (typically $< 0.05$) is evidence that the predictor has a non-zero effect.
- **Introduced in:** L11 (slide 19).
- **Reused in:** L11 (slides 20–21, 36, 44 — interpreting regression output).
- **Alternative names seen in source:** —
- **Notation:** $p$.

## Path (search)

- **Definition:** Sequence of actions (or states) leading from one state to another in the search graph; a solution is a path from the initial state to a goal state.
- **Introduced in:** L03 (slide 10).
- **Reused in:** L03 (every search algorithm).
- **Alternative names seen in source:** —
- **Notation:** —

## Path cost

- **Definition:** Sum of the step costs along a path; the optimal solution minimises path cost. The slides assume non-negative step costs throughout.
- **Introduced in:** L03 (slide 10).
- **Reused in:** L03 (UCS expands by path cost, slide 36), L07 (constant per step in standard CSP formulation, slide 7).
- **Alternative names seen in source:** —
- **Notation:** $g(n)$.

## PEAS (Performance, Environment, Actuators, Sensors)

- **Definition:** Four-component specification of a task environment. Naming PEAS pins down what the agent must achieve, what it acts on, how it acts, and what it can sense.
- **Introduced in:** L02 (slide 14; taxi example slide 14; spam-filter example slide 15).
- **Reused in:** —
- **Alternative names seen in source:** "Task Environment Specification" (L02 slide 14).
- **Notation:** —

## Percept

- **Definition:** A single perceptual input received by an agent at a moment in time. A percept may be a single sensor reading or a structured tuple of all sensor readings at that time.
- **Introduced in:** L02 (slide 6).
- **Reused in:** L02 (every agent example), L03 (problem-solving agent ignores percepts during execution, slide 9).
- **Alternative names seen in source:** —
- **Notation:** —

## Percept sequence

- **Definition:** The complete history of everything the agent has perceived from its activation up to the present moment. The agent function maps percept sequences (not single percepts) to actions.
- **Introduced in:** L02 (slide 6).
- **Reused in:** L02 (table-driven agent stores percept-sequence → action table, slide 25; learning agent builds it incrementally).
- **Alternative names seen in source:** —
- **Notation:** $P^{*}$.

## Performance measure

- **Definition:** Objective external criterion for assessing how well an agent is doing — defined by the designer, in terms of the environment, not the agent's internal mental states. A rational agent maximises its expected performance measure.
- **Introduced in:** L02 (slide 10).
- **Reused in:** L02 (every PEAS example), L09a (slide 3 — expected utility is the probabilistic generalisation).
- **Alternative names seen in source:** "utility function" (L02 slide 10).
- **Notation:** —

## Polynomial regression

- **Definition:** Regression model in which the response is a polynomial in one (or more) predictors — typically obtained by adding $x^2, x^3, \dots$ as features to a linear regression. Higher degree fits more flexible curves but risks overfitting.
- **Introduced in:** Not formally introduced in the L11 slide deck (the slides cover linear regression with dummy variables and interaction terms, and frame "flexible regression" via interactions). Listed in the syllabus and used in ML Lab 2. **Flagged for canonicalisation** (see open questions).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** $y = a + b_1 x + b_2 x^2 + \dots$

## Population (genetic algorithm)

- **Definition:** Set of chromosomes considered together in one generation. Typical sizes 50–500; larger populations explore more but cost more per generation.
- **Introduced in:** L05 (slides 26, 41, 47).
- **Reused in:** L05 (every later slide).
- **Alternative names seen in source:** —
- **Notation:** $N$.

## Posterior probability

- **Definition:** Conditional distribution $P(X \mid e)$ over a query variable given evidence; the output of probabilistic inference. Bayes' rule converts a prior plus a likelihood into a posterior.
- **Introduced in:** L09a (slide 43 — "$P(X \mid E)$").
- **Reused in:** L09b (smoothing yields the posterior over hidden states given the entire observation sequence).
- **Alternative names seen in source:** —
- **Notation:** $P(X \mid e)$.

## Prior probability

- **Definition:** Unconditional distribution $P(X)$ over a variable before observing any evidence. In a Bayesian network, the priors of root nodes appear directly in the CPTs as $P(X)$ tables; in an HMM the initial distribution $\pi$ plays this role.
- **Introduced in:** L09a (slides 35–36 — root-node CPT $P(A)$).
- **Reused in:** L09b (slide 2 — "Priors (initial state probabilities)").
- **Alternative names seen in source:** —
- **Notation:** $P(X)$.

## Problem-solving agent

- **Definition:** Goal-based agent that, when the right action is not obvious, plans a sequence of actions reaching a goal by searching through the state space.
- **Introduced in:** L03 (slide 4).
- **Reused in:** L03 (every search algorithm builds this agent), L05 (local-search relaxation), L07 (CSP variant).
- **Alternative names seen in source:** —
- **Notation:** —

## R-squared ($R^2$)

- **Definition:** Goodness-of-fit measure for a regression model: $R^2 = \text{SSR} / \text{SST} = 1 - \text{SSE} / \text{SST}$. Equals the proportion of total variance in the response explained by the model; ranges 0–1.
- **Introduced in:** L11 (slides 12–18).
- **Reused in:** L11 (slide 44 — comparing nested models; slide 18 — adjusted-$R^2$).
- **Alternative names seen in source:** "Multiple R-squared" (L11 slide 12).
- **Notation:** $R^2$.

## Random forest

- **Definition:** Ensemble of decision trees, each trained on a bootstrap sample of the data and a random subset of the features at every split; predictions are aggregated by majority vote (classification) or averaging (regression). Reduces the variance of individual trees.
- **Introduced in:** L10 (slide 20).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Random restart hill climbing

- **Definition:** Hill-climbing variant that, on reaching a local maximum, restarts from a fresh random state and keeps the best solution seen across all restarts.
- **Introduced in:** L05 (slide 15).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Random variable

- **Definition:** Function from the sample space of a random experiment to the real numbers; equivalently, a variable whose value reflects the outcome of a probabilistic process. Domains must be mutually exclusive and exhaustive.
- **Introduced in:** L09a (slides 5–6).
- **Reused in:** L09a (every later slide), L09b (hidden state and observation are random variables).
- **Alternative names seen in source:** —
- **Notation:** Capital letters $X, Y, R, W$.

## Rational agent

- **Definition:** An agent that, for every percept sequence, selects an action expected to maximise its performance measure, given the evidence in the percept sequence and its built-in knowledge.
- **Introduced in:** L02 (slide 10).
- **Reused in:** L02 (every later agent type is a different implementation strategy for rationality); L09a (slide 3 — extension to probabilistic rationality).
- **Alternative names seen in source:** —
- **Notation:** —

## Reflex agent (simple reflex agent)

- **Definition:** Agent whose action depends only on the current percept, implemented as condition-action rules. Requires a fully observable environment to behave correctly.
- **Introduced in:** L02 (slides 27–28).
- **Reused in:** L02 (model-based reflex agent extends it for partial observability, slides 29–30).
- **Alternative names seen in source:** —
- **Notation:** —

## Regression

- **Definition:** Supervised-learning task in which the model maps inputs to a continuous-valued output. Contrasted with classification, which has discrete outputs.
- **Introduced in:** L10 (slide 10).
- **Reused in:** L11 (entire lecture).
- **Alternative names seen in source:** —
- **Notation:** —

## Reinforcement learning (RL)

- **Definition:** Learning paradigm in which an agent interacts with an environment, takes actions, observes rewards, and adapts its policy to maximise cumulative reward. Unlike supervised learning, there is no pre-labelled dataset — the agent must explore.
- **Introduced in:** L10 (slides 5–7).
- **Reused in:** L06 (slide 40 — TD-Gammon used RL to learn its evaluation function).
- **Alternative names seen in source:** "RL".
- **Notation:** —

## Residual (regression)

- **Definition:** Difference between an observed response value and the value predicted by the regression model: $r_i = y_i - \hat{y}_i$. OLS fits the model that minimises $\sum_i r_i^2$.
- **Introduced in:** L11 (slide 10).
- **Reused in:** L11 (slides 13–15 — SST, SSE, SSR derivation).
- **Alternative names seen in source:** —
- **Notation:** —

## Roulette-wheel selection

- **Definition:** Fitness-proportionate selection rule for a GA: each chromosome's probability of being selected as a parent is proportional to its fitness. Implemented by sampling a uniform random number in $[0, \sum_i f_i]$ and walking a cumulative-sum list.
- **Introduced in:** L05 (slides 40–42).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Search strategy

- **Definition:** Rule determining the order in which the search algorithm picks nodes to expand from the frontier. The strategy is what distinguishes BFS, DFS, UCS, IDS, A*, etc.
- **Introduced in:** L03 (slide 27).
- **Reused in:** L03 (every algorithm is a different strategy), L06 (minimax + alpha-beta is the adversarial strategy).
- **Alternative names seen in source:** —
- **Notation:** —

## Search tree

- **Definition:** Tree whose root is the initial state and whose children of a node are the states reachable from that node by one action. Every search algorithm explores some portion of the search tree.
- **Introduced in:** L03 (slide 20).
- **Reused in:** L03 (every example), L06 (game tree is the adversarial analogue).
- **Alternative names seen in source:** —
- **Notation:** —

## Simulated annealing

- **Definition:** Local-search variant that probabilistically accepts moves that *worsen* the objective, with probability $\exp(\Delta / T)$ that decreases as temperature $T$ is lowered on an annealing schedule. Designed to escape local maxima; converges to the global optimum in the limit of an infinitely slow schedule.
- **Introduced in:** L05 (slides 16–20).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** $T$ (temperature).

## Single agent (environment property)

- **Definition:** The environment contains only one acting agent — no others whose actions affect performance.
- **Introduced in:** L02 (slide 22).
- **Reused in:** L02 (slides 23–24), L06 (contrast — games are multi-agent, slide 3).
- **Alternative names seen in source:** —
- **Notation:** —

## State

- **Definition:** Representation of one configuration of the world relevant to the agent's reasoning. In search, the state space is the directed graph of all states reachable from the initial state via actions.
- **Introduced in:** L02 (slide 6 — implicit; explicit in L03 slide 10).
- **Reused in:** L03 (every search algorithm), L05, L06, L07 (CSP state is the current assignment), L09b (hidden state).
- **Alternative names seen in source:** "configuration" (L03 slide 20).
- **Notation:** $s$.

## State space

- **Definition:** Set of all states reachable from the initial state by any sequence of actions; equivalently, the directed graph whose nodes are states and edges are actions. The size of the state space determines the difficulty of search.
- **Introduced in:** L03 (slide 12).
- **Reused in:** L05 (slide 30 — "search space or state space"), L06 (game-tree state space), L07 (CSP state space).
- **Alternative names seen in source:** "search space" (L05 slide 30, L07 slide 2).
- **Notation:** —

## Static vs dynamic (environment property)

- **Definition:** A static environment does not change while the agent is deciding what to do; a dynamic environment can change during deliberation.
- **Introduced in:** L02 (slide 20).
- **Reused in:** L02 (slides 23–24), L06 (chess-with-clock is dynamic).
- **Alternative names seen in source:** —
- **Notation:** —

## Stochastic hill climbing

- **Definition:** Hill-climbing variant that, instead of always picking the best successor, picks among improving successors (or the first improvement found). Useful when computing all successors is expensive.
- **Introduced in:** L05 (slide 13 — "Variants: choose first better successor, randomly choose among better successors").
- **Reused in:** —
- **Alternative names seen in source:** "first-choice hill climbing".
- **Notation:** —

## Successor function

- **Definition:** Function $\text{SUCC}(s)$ that returns the set of (action, resulting-state) pairs reachable from state $s$. Together with initial state, goal test, and step cost it defines a search problem.
- **Introduced in:** L03 (slide 10).
- **Reused in:** L03, L05 (slide 11 — for n-queens), L06 (children in the game tree), L07 (assigning a value to an unassigned variable, slide 7).
- **Alternative names seen in source:** "operator" (L03 slide 5).
- **Notation:** —

## Sum of squares — total (SST), error (SSE), regression (SSR)

- **Definition:** Three variance-decomposition quantities for linear regression. $\text{SST} = \sum (y_i - \bar{y})^2$ is the total variability in the response; $\text{SSE} = \sum (y_i - \hat{y}_i)^2$ is the variability the model fails to explain (sum of squared residuals); $\text{SSR} = \text{SST} - \text{SSE}$ is the variability the regression captures.
- **Introduced in:** L11 (slides 13–15).
- **Reused in:** L11 ($R^2 = \text{SSR}/\text{SST}$, slide 15).
- **Alternative names seen in source:** "sum of squared errors", "total sum of squares" (L11 slides 13–15).
- **Notation:** SST, SSE, SSR.

## Supervised learning

- **Definition:** Learning paradigm in which the training data consists of input/output pairs and the model learns the mapping. Splits into classification (discrete output) and regression (continuous output).
- **Introduced in:** L10 (slides 8–9).
- **Reused in:** L10 (every classification method, slides 17–60), L11 (regression is its continuous incarnation).
- **Alternative names seen in source:** —
- **Notation:** —

## Temperature schedule (simulated annealing)

- **Definition:** Function $T(t)$ that decreases the temperature over time. Slow cooling gives stronger convergence guarantees at the cost of runtime; typical schedules are linear, geometric ($T(t) = T_0 \cdot \alpha^t$), or logarithmic.
- **Introduced in:** L05 (slides 17–18).
- **Reused in:** —
- **Alternative names seen in source:** "annealing schedule" (L05 slide 16).
- **Notation:** $T(t)$.

## Terminal state (game tree)

- **Definition:** A state in which the game is over; the terminal-utility (or terminal-test + utility) function assigns each terminal state a payoff for the MAX player.
- **Introduced in:** L06 (slides 11, 14).
- **Reused in:** L06 (alpha-beta still backs values up from terminal nodes, slides 22–35).
- **Alternative names seen in source:** —
- **Notation:** —

## Test set

- **Definition:** Held-out portion of the data used only to evaluate the trained model's generalisation performance. Distinct from the training set (used to fit) and the (optional) validation set (used to tune hyperparameters).
- **Introduced in:** L10 (slide 18).
- **Reused in:** L10 (slide 56 — overfitting is diagnosed by comparing train- and test-error).
- **Alternative names seen in source:** —
- **Notation:** —

## Training set

- **Definition:** Data used to fit the parameters of a supervised model. Performance on the training set is not, by itself, a good estimate of future performance — see overfitting.
- **Introduced in:** L10 (slide 18).
- **Reused in:** L10 (slides 19, 33, 56).
- **Alternative names seen in source:** —
- **Notation:** —

## Transition model (Markov chain / HMM)

- **Definition:** Matrix $A$ with entries $a_{ij} = P(q_t = j \mid q_{t-1} = i)$ giving the probability of moving from hidden state $i$ to hidden state $j$ in one time step. Rows of $A$ sum to 1.
- **Introduced in:** L09b (slides 2, 9, 23).
- **Reused in:** L09b (forward, Viterbi recursions, slides 36–48).
- **Alternative names seen in source:** "transition probabilities" / "transition probability matrix" (L09b slide 9).
- **Notation:** $A$, $a_{ij}$.

## Transition model (search)

- **Definition:** Function $\text{Result}(s, a)$ giving the state that follows from taking action $a$ in state $s$ — the deterministic search counterpart of the HMM transition model.
- **Introduced in:** L03 (slide 10 — embedded in the successor function definition).
- **Reused in:** L02 (model-based reflex agent, slide 30).
- **Alternative names seen in source:** "successor function" (L03 slide 10), "operator" (L03 slide 5).
- **Notation:** —

## Uncertainty

- **Definition:** Property of environments where deterministic logical inference is insufficient because the agent has partial observability, stochastic action outcomes, or lacks computational resources to model fully. Quantified using probabilities.
- **Introduced in:** L09a (slide 2).
- **Reused in:** L09a (every later slide), L09b (HMM is a model of uncertainty over time), L10 (RL slide 7 — stochastic rewards).
- **Alternative names seen in source:** —
- **Notation:** —

## Uniform-cost search (UCS)

- **Definition:** Uninformed search that expands the unexpanded node with the lowest path cost $g(n)$, using a priority queue. Complete; optimal when step costs are non-negative; reduces to BFS when all step costs are equal.
- **Introduced in:** L03 (slides 36–37).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Uninformed search

- **Definition:** Class of search strategies that use only the information explicitly given in the problem definition — no heuristic estimates of distance-to-goal. Includes BFS, DFS, UCS, and IDS.
- **Introduced in:** L03 (slides 1, 29).
- **Reused in:** L05, L06, L07 (each introduces a more specialised search technique by contrast).
- **Alternative names seen in source:** "blind search".
- **Notation:** —

## Unsupervised learning

- **Definition:** Learning paradigm with no labelled outputs; the algorithm must discover structure in the data itself. Includes clustering, outlier detection, density estimation.
- **Introduced in:** L10 (slide 4).
- **Reused in:** L12 (clustering is the principal unsupervised method covered).
- **Alternative names seen in source:** —
- **Notation:** —

## Utility-based agent

- **Definition:** Agent that uses a utility function mapping states (or sequences of states) to real numbers, allowing it to compare states by desirability rather than only checking goal-or-not. Required when there are multiple ways to satisfy a goal and we want the best one.
- **Introduced in:** L02 (slide 32).
- **Reused in:** L09a (slide 3 — expected-utility decision making).
- **Alternative names seen in source:** —
- **Notation:** —

## Utility function

- **Definition:** Function $U : S \to \mathbb{R}$ assigning a real-valued desirability to each world state. In games, $U(s)$ is the payoff at terminal states; in decision theory it is what a rational agent maximises in expectation.
- **Introduced in:** L02 (slide 10 — "performance measure (utility function)"; slide 32 utility-based agent).
- **Reused in:** L06 (slide 6 — game utility; slides 11–17 — terminal utility), L09a (slide 3 — expected utility).
- **Alternative names seen in source:** "performance measure" (L02 slide 10), "evaluation function" (L06 slide 30 — non-terminal estimate).
- **Notation:** $U$.

## Variable (CSP)

- **Definition:** A symbol $X_i$ in a CSP that must be assigned exactly one value from its domain $D_i$ in any solution.
- **Introduced in:** L07 (slide 6).
- **Reused in:** L07 (every example), L09a (random variable is the probabilistic analogue, slide 5).
- **Alternative names seen in source:** —
- **Notation:** $X_i$.

## Variable domain (CSP)

- **Definition:** Set $D_i$ of values that variable $X_i$ is allowed to take in a CSP solution. May be finite (map-colouring), continuous (scheduling), or numeric (cryptarithmetic).
- **Introduced in:** L07 (slide 6).
- **Reused in:** L07 (forward checking and arc consistency prune domains).
- **Alternative names seen in source:** "domain" (L07 slide 6).
- **Notation:** $D_i$.

## Viterbi algorithm

- **Definition:** Dynamic-programming algorithm that finds the single most likely hidden state sequence given the observation sequence and HMM model. Same structure as the forward algorithm but uses $\max$ in place of $\sum$ and keeps backpointers so the sequence can be recovered by back-tracing.
- **Introduced in:** L09b (slides 44–51).
- **Reused in:** —
- **Alternative names seen in source:** —
- **Notation:** —

## Zero-sum game

- **Definition:** Two-player game in which the sum of the players' utilities at any terminal state is constant (typically 0): one player's gain is exactly the other's loss. Standard model for chess, checkers, Go, Tic-Tac-Toe.
- **Introduced in:** L06 (slide 6).
- **Reused in:** L06 (every later slide).
- **Alternative names seen in source:** —
- **Notation:** —

---

## Open canonicalisation questions

The following ambiguities surfaced during the shallow skim. Lecture Extractors (Wave 1) should treat these as flagged and use the choices noted below unless they find evidence in the deep read that contradicts the choice. The PM will arbitrate any conflicts.

1. **A\* / admissibility / consistency / greedy best-first.** L03's objectives slide (p.7) lists "informed search — best-first (greedy, A*), heuristics" but L03 ends (slide 54) with the comment "These two haven't covered, but you can read about them in the book." A* is therefore *referenced* but not *derived* anywhere in the 10-lecture deck. The lab handouts (Lab 2 — Search) may treat A* as known. **Recommendation:** Lecture Extractor for L03 should include a §3.x "A* and informed search (forward reference)" sub-section so the cheat sheet covers the term; the rigorous derivation can live in the L05 chapter alongside hill climbing, since L05 is the first place where a heuristic function is concretely used. Add "admissibility" and "consistency" entries to the glossary in Wave 2 once the depth is confirmed.

2. **Polynomial regression.** The plan lists polynomial regression as a target concept. L11 spends its "flexible models" section (slides 22–46) on dummy variables and interaction terms rather than polynomial features per se. ML Lab 2 — Regression is named "Regression" with a "Higher polynomial degree" variant in §8.3 of the spec, implying ML Lab 2 introduces polynomial features. **Recommendation:** keep the placeholder glossary entry; the Lab Solver for ML Lab 2 should write up polynomial regression and the Wave-2 Index Builder can promote it to a proper canonical entry.

3. **Gradient descent / MSE / RMSE.** The L11 slides use Sum of Squared Errors and OLS via the normal equation but never mention gradient descent or the metric names MSE / RMSE explicitly (slides instead use the un-normalised SSE / SST / R²). These almost certainly appear in ML Lab 2. **Recommendation:** the Wave-2 Index Builder, after ML Lab 2 is locked, should add canonical entries for gradient descent, MSE, RMSE, learning rate, epoch.

4. **Elbow method / silhouette score / K-means++.** The plan lists these as expected ML Lab 3 — Clustering concepts. L12's slide deck covers K-means iteration, hierarchical, and DBSCAN but does not formally name the elbow method or silhouette score; "Bisecting K-means" (slide 18) is mentioned as a robustness fix but K-means++ initialisation is not. **Recommendation:** placeholder glossary entries to be added in Wave 2 once ML Lab 3 is locked; the lab notebook is the probable canonical source.

5. **Validation set / cross-validation / hyperparameter / stratified split.** L10 covers train/test split but never names a validation set or cross-validation. Hyperparameters appear obliquely on slide 53 ("Early termination using hyperparameters such as max_depth..."). **Recommendation:** include glossary entries here for completeness — Lab Solvers for ML Labs 1–3 will need them — but mark them as "not formally introduced in any lecture" so Wave-1 Lecture Extractors do not over-claim coverage.

6. **AC-3 vs "arc consistency".** L07 slides never use the name "AC-3" explicitly, but the algorithm depicted on slides 46–52 is AC-3 (re-queueing arcs whenever a domain shrinks). **Recommendation:** use "Arc consistency / AC-3" as a combined canonical name in chapter headings; do not assume the lecturer used the textbook abbreviation.

7. **Filtering / smoothing / prediction (HMM problems 1, 2, 3).** L09b uses the textbook names "Evaluation" (problem 1), "Decoding" (problem 2), "Learning" (problem 3) — not the more common "filtering / smoothing / Viterbi / Baum-Welch" quartet. **Recommendation:** Lecture Extractor for L09b should give *both* names side by side and the glossary entries here use the slide-aligned name in the headline.

8. **Naive Bayes — L09a vs L10.** The Naive Bayes classifier is introduced in L09a (slides 27–29) before Bayesian networks proper, and is also listed in L10's classification-techniques slide (p.20). **Recommendation:** "Introduced in: L09a"; the L10 reference is a "Reused in" cross-link.

9. **"Operator" vs "successor function" vs "transition model".** All three names appear across L02, L03, and L09b for closely related concepts. **Recommendation:** canonical name in the search context is "successor function" (since the L03 slide defines it with that header); "operator" is the alternative; "transition model" is reserved for the probabilistic (Markov / HMM) sense.

10. **"Heuristic function" vs "evaluation function" vs "objective function".** The slides use "heuristic" in L03/L05 (search), "evaluation function" in L06 (adversarial), and "objective function" in L05 (local search). They are closely related but not interchangeable. **Recommendation:** keep all three glossary entries distinct; cross-link them via "Alternative names seen in source".
