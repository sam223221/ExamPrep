/**
 * Type definitions for a discrete Bayesian network.
 *
 * Framework-free — no React, no DOM. These types are shared by the pure
 * inference engine (`inference.ts`) and by the UI layer, but they describe
 * only the mathematical model.
 *
 * Modelling decisions (mirroring the course `Variable.py` formulation):
 *   - Each node owns an ordered list of discrete `states` (its domain).
 *   - Each node lists its `parents` by id, in a FIXED order. That order is the
 *     order parent-state values appear in CPT keys.
 *   - A CPT maps the tuple of parent-state assignments (joined into a string
 *     key, in parent order) to a probability distribution aligned to this
 *     node's `states` order. Roots use the empty-tuple key (`""`).
 */

/** A conditional probability distribution over one node's states. */
export type Distribution = number[];

/**
 * Conditional probability table.
 *
 * Key = the parent-state assignment encoded with {@link cptKey} (parent order,
 * joined by the unit-separator character). Value = a {@link Distribution}
 * aligned to the node's `states` order. Each value should sum to 1.
 *
 * For a root node (no parents) the single key is the empty string `""`.
 */
export type Cpt = Record<string, Distribution>;

/** A single random-variable node in the network. */
export interface BNNode {
  /** Stable unique identifier. Used in edges, CPT lookups and evidence maps. */
  id: string;
  /** Human-readable name (defaults to the id; editable in the UI). */
  name: string;
  /** Ordered discrete domain, e.g. `["true", "false"]`. Minimum length 2. */
  states: string[];
  /** Parent node ids in CPT-key order. */
  parents: string[];
  /** Conditional probability table keyed by encoded parent assignments. */
  cpt: Cpt;
}

/** Directed parent -> child edge (kept for the UI; parents are the source of truth). */
export interface BNEdge {
  id: string;
  source: string;
  target: string;
}

/** A complete Bayesian network: an ordered collection of nodes. */
export interface BayesNetworkModel {
  nodes: BNNode[];
}

/** Evidence / full assignment: node id -> chosen state. */
export type Assignment = Record<string, string>;

/**
 * Unit-separator control character (U+001F) used to join parent-state tuples
 * into a single CPT key. It is built from a char code so it survives editors
 * that strip raw control characters, and it can never appear inside a normal
 * state name typed by a user.
 */
const KEY_SEPARATOR = String.fromCharCode(31);

/**
 * Encode a parent-state tuple into a stable CPT key.
 *
 * The values must be supplied in parent order. An empty array yields `""`,
 * the canonical root key.
 */
export function cptKey(parentStates: readonly string[]): string {
  return parentStates.join(KEY_SEPARATOR);
}

/** Decode a CPT key back into its ordered parent-state tuple. */
export function parseCptKey(key: string): string[] {
  return key === '' ? [] : key.split(KEY_SEPARATOR);
}
