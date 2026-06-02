/**
 * Exact inference for discrete Bayesian networks by enumeration.
 *
 * Pure TypeScript — no React, no DOM. Implements AIMA's ENUMERATION-ASK /
 * ENUMERATE-ALL (Russell & Norvig, 3rd ed., §14.4), plus helpers for
 * topological ordering with cycle detection, marginals and full-joint lookup.
 *
 * The algorithm is exponential in the number of hidden variables, which is
 * acceptable for exam-sized networks (the documented scope of this tool).
 */

import {
  type Assignment,
  type BayesNetworkModel,
  type BNNode,
  type Distribution,
  cptKey,
} from './types';

/** Index a network's nodes by id for O(1) lookup. */
function indexById(network: BayesNetworkModel): Map<string, BNNode> {
  const map = new Map<string, BNNode>();
  for (const node of network.nodes) {
    map.set(node.id, node);
  }
  return map;
}

/**
 * Return node ids in topological order (every parent precedes its children).
 *
 * Uses Kahn's algorithm over the parent relation. Throws if the graph contains
 * a cycle (a Bayesian network must be a DAG) or references a missing parent.
 */
export function topologicalOrder(network: BayesNetworkModel): string[] {
  const byId = indexById(network);

  // Validate parent references up front for clear error messages.
  for (const node of network.nodes) {
    for (const parentId of node.parents) {
      if (!byId.has(parentId)) {
        throw new Error(
          `Node "${node.id}" references unknown parent "${parentId}".`,
        );
      }
    }
  }

  // In-degree = number of parents each node still waits on.
  const inDegree = new Map<string, number>();
  // Adjacency: parent id -> ids of its children.
  const children = new Map<string, string[]>();
  for (const node of network.nodes) {
    inDegree.set(node.id, node.parents.length);
    if (!children.has(node.id)) children.set(node.id, []);
  }
  for (const node of network.nodes) {
    for (const parentId of node.parents) {
      children.get(parentId)!.push(node.id);
    }
  }

  // Seed the queue with roots, preserving declaration order for stable output.
  const queue: string[] = [];
  for (const node of network.nodes) {
    if (inDegree.get(node.id) === 0) queue.push(node.id);
  }

  const ordered: string[] = [];
  while (queue.length > 0) {
    const id = queue.shift()!;
    ordered.push(id);
    for (const childId of children.get(id) ?? []) {
      const remaining = (inDegree.get(childId) ?? 0) - 1;
      inDegree.set(childId, remaining);
      if (remaining === 0) queue.push(childId);
    }
  }

  if (ordered.length !== network.nodes.length) {
    throw new Error('Bayesian network contains a cycle; it must be a DAG.');
  }
  return ordered;
}

/**
 * Look up `P(node = value | parents = values-in-assignment)` from a node's CPT.
 *
 * The assignment must contain a value for every parent of `node`. Throws if a
 * parent value is missing, the CPT row is absent, or `value` is not a state.
 */
export function conditionalProbability(
  node: BNNode,
  value: string,
  assignment: Assignment,
): number {
  const stateIndex = node.states.indexOf(value);
  if (stateIndex < 0) {
    throw new Error(`State "${value}" is not a value of node "${node.id}".`);
  }

  const parentStates = node.parents.map((parentId) => {
    const parentValue = assignment[parentId];
    if (parentValue === undefined) {
      throw new Error(
        `Cannot evaluate node "${node.id}": parent "${parentId}" has no value.`,
      );
    }
    return parentValue;
  });

  const row = node.cpt[cptKey(parentStates)];
  if (!row) {
    throw new Error(
      `CPT for node "${node.id}" has no row for parents [${parentStates.join(', ')}].`,
    );
  }
  const probability = row[stateIndex];
  if (probability === undefined) {
    throw new Error(
      `CPT row for node "${node.id}" is missing a value for state "${value}".`,
    );
  }
  return probability;
}

/**
 * AIMA ENUMERATE-ALL.
 *
 * @param vars     Node ids in topological order, not yet consumed.
 * @param index    Current position in `vars` (recursion cursor).
 * @param evidence Partial assignment built up so far.
 * @param byId     Lookup of node id -> node.
 * @returns The summed product of conditional probabilities for this branch.
 */
function enumerateAll(
  vars: string[],
  index: number,
  evidence: Assignment,
  byId: Map<string, BNNode>,
): number {
  if (index >= vars.length) return 1.0;

  const node = byId.get(vars[index]!)!;
  const known = evidence[node.id];

  if (known !== undefined) {
    // Y is fixed in the evidence: multiply its conditional and recurse.
    return (
      conditionalProbability(node, known, evidence) *
      enumerateAll(vars, index + 1, evidence, byId)
    );
  }

  // Y is hidden: sum over its possible values.
  let total = 0;
  for (const value of node.states) {
    const extended: Assignment = { ...evidence, [node.id]: value };
    total +=
      conditionalProbability(node, value, extended) *
      enumerateAll(vars, index + 1, extended, byId);
  }
  return total;
}

/**
 * AIMA ENUMERATION-ASK: the posterior distribution `P(queryVar | evidence)`.
 *
 * For each value `x` of the query variable, extends the evidence with
 * `queryVar = x`, runs ENUMERATE-ALL over all variables in topological order,
 * then normalizes the resulting vector.
 *
 * @throws if the network has a cycle, the query variable is unknown, evidence
 *         references an unknown node/state, or the unnormalized mass is zero
 *         (an impossible/contradictory evidence set).
 */
export function enumerationAsk(
  queryVar: string,
  evidence: Assignment,
  network: BayesNetworkModel,
): Record<string, number> {
  const byId = indexById(network);
  const query = byId.get(queryVar);
  if (!query) {
    throw new Error(`Query variable "${queryVar}" is not in the network.`);
  }

  // Validate the evidence assignment before doing any work.
  for (const [id, value] of Object.entries(evidence)) {
    const node = byId.get(id);
    if (!node) {
      throw new Error(`Evidence references unknown node "${id}".`);
    }
    if (!node.states.includes(value)) {
      throw new Error(
        `Evidence value "${value}" is not a state of node "${id}".`,
      );
    }
  }

  const order = topologicalOrder(network);

  const unnormalized: Distribution = query.states.map((value) => {
    const extended: Assignment = { ...evidence, [queryVar]: value };
    return enumerateAll(order, 0, extended, byId);
  });

  const total = unnormalized.reduce((sum, p) => sum + p, 0);
  if (total <= 0) {
    throw new Error(
      `Inference failed: evidence has zero probability under the model (impossible evidence).`,
    );
  }

  const result: Record<string, number> = {};
  query.states.forEach((value, i) => {
    result[value] = unnormalized[i]! / total;
  });
  return result;
}

/**
 * The marginal distribution `P(queryVar)` — enumeration with empty evidence.
 */
export function marginal(
  queryVar: string,
  network: BayesNetworkModel,
): Record<string, number> {
  return enumerationAsk(queryVar, {}, network);
}

/**
 * Full-joint probability of a complete assignment:
 * `P(x1, …, xn) = Π P(xi | parents(xi))`.
 *
 * @throws if the assignment omits a node, names an unknown node, or uses a
 *         value outside a node's domain.
 */
export function jointProbability(
  assignment: Assignment,
  network: BayesNetworkModel,
): number {
  const byId = indexById(network);

  for (const id of Object.keys(assignment)) {
    if (!byId.has(id)) {
      throw new Error(`Assignment references unknown node "${id}".`);
    }
  }

  let product = 1;
  for (const node of network.nodes) {
    const value = assignment[node.id];
    if (value === undefined) {
      throw new Error(
        `Full-joint requires a value for every node; "${node.id}" is missing.`,
      );
    }
    if (!node.states.includes(value)) {
      throw new Error(
        `Value "${value}" is not a state of node "${node.id}".`,
      );
    }
    product *= conditionalProbability(node, value, assignment);
  }
  return product;
}

/**
 * Validate that every CPT row of every node sums to 1 (within tolerance) and
 * has one entry per state. Returns a list of human-readable problems; empty
 * means the network's CPTs are well-formed. Used by the UI to surface a clear
 * "network invalid" message without throwing.
 */
export function validateCpts(
  network: BayesNetworkModel,
  tolerance = 1e-6,
): string[] {
  const problems: string[] = [];
  for (const node of network.nodes) {
    const rows = Object.values(node.cpt);
    if (rows.length === 0) {
      problems.push(`"${node.name}" has no CPT rows.`);
      continue;
    }
    for (const row of rows) {
      if (row.length !== node.states.length) {
        problems.push(
          `"${node.name}" CPT row has ${row.length} values but ${node.states.length} states.`,
        );
        continue;
      }
      const sum = row.reduce((acc, p) => acc + p, 0);
      if (Math.abs(sum - 1) > tolerance) {
        problems.push(
          `"${node.name}" CPT row sums to ${sum.toFixed(4)} (must be 1).`,
        );
      }
      if (row.some((p) => p < 0 || p > 1 || Number.isNaN(p))) {
        problems.push(`"${node.name}" CPT row has a value outside [0, 1].`);
      }
    }
  }
  return problems;
}

/**
 * Returns `true` when the network is a DAG (no cycles, no missing parents).
 * Non-throwing wrapper around {@link topologicalOrder} for UI use.
 */
export function isDag(network: BayesNetworkModel): boolean {
  try {
    topologicalOrder(network);
    return true;
  } catch {
    return false;
  }
}
