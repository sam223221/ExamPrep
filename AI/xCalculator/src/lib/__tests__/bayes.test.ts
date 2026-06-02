import { describe, it, expect } from 'vitest';
import {
  enumerationAsk,
  marginal,
  jointProbability,
  topologicalOrder,
  validateCpts,
} from '../bayes/inference';
import { type BayesNetworkModel, cptKey } from '../bayes/types';

/**
 * Build the canonical AIMA Alarm/Burglary network in code (Russell & Norvig,
 * Figure 14.2). Distributions are aligned to the `["true", "false"]` order.
 */
function alarmNetwork(): BayesNetworkModel {
  const TF = ['true', 'false'];
  return {
    nodes: [
      {
        id: 'Burglary',
        name: 'Burglary',
        states: [...TF],
        parents: [],
        cpt: { [cptKey([])]: [0.001, 0.999] },
      },
      {
        id: 'Earthquake',
        name: 'Earthquake',
        states: [...TF],
        parents: [],
        cpt: { [cptKey([])]: [0.002, 0.998] },
      },
      {
        id: 'Alarm',
        name: 'Alarm',
        states: [...TF],
        parents: ['Burglary', 'Earthquake'],
        cpt: {
          [cptKey(['true', 'true'])]: [0.95, 0.05],
          [cptKey(['true', 'false'])]: [0.94, 0.06],
          [cptKey(['false', 'true'])]: [0.29, 0.71],
          [cptKey(['false', 'false'])]: [0.001, 0.999],
        },
      },
      {
        id: 'JohnCalls',
        name: 'JohnCalls',
        states: [...TF],
        parents: ['Alarm'],
        cpt: {
          [cptKey(['true'])]: [0.9, 0.1],
          [cptKey(['false'])]: [0.05, 0.95],
        },
      },
      {
        id: 'MaryCalls',
        name: 'MaryCalls',
        states: [...TF],
        parents: ['Alarm'],
        cpt: {
          [cptKey(['true'])]: [0.7, 0.3],
          [cptKey(['false'])]: [0.01, 0.99],
        },
      },
    ],
  };
}

describe('Bayesian network — exact inference by enumeration', () => {
  it('reproduces AIMA P(Burglary=true | JohnCalls=true, MaryCalls=true) ≈ 0.284', () => {
    const net = alarmNetwork();
    const posterior = enumerationAsk(
      'Burglary',
      { JohnCalls: 'true', MaryCalls: 'true' },
      net,
    );
    expect(posterior.true).toBeCloseTo(0.284, 3);
  });

  it('returns a normalized distribution that sums to 1', () => {
    const net = alarmNetwork();
    const posterior = enumerationAsk(
      'Burglary',
      { JohnCalls: 'true', MaryCalls: 'true' },
      net,
    );
    const sum = posterior.true + posterior.false;
    expect(sum).toBeCloseTo(1, 10);
    expect(posterior.false).toBeCloseTo(1 - 0.2841718, 5);
  });

  it('computes a small marginal P(Alarm=true) ≈ 0.0025', () => {
    const net = alarmNetwork();
    const m = marginal('Alarm', net);
    expect(m.true).toBeCloseTo(0.002516, 5);
    expect(m.true + m.false).toBeCloseTo(1, 10);
  });

  it('computes the marginal P(Burglary=true) = 0.001 with empty evidence', () => {
    const net = alarmNetwork();
    const m = marginal('Burglary', net);
    expect(m.true).toBeCloseTo(0.001, 10);
  });

  it('computes a full-joint probability by the chain rule', () => {
    const net = alarmNetwork();
    // P(j, m, a, ¬b, ¬e) = 0.90 * 0.70 * 0.001 * 0.999 * 0.998  (AIMA p.514)
    const joint = jointProbability(
      {
        JohnCalls: 'true',
        MaryCalls: 'true',
        Alarm: 'true',
        Burglary: 'false',
        Earthquake: 'false',
      },
      net,
    );
    const expected = 0.9 * 0.7 * 0.001 * 0.999 * 0.998;
    expect(joint).toBeCloseTo(expected, 12);
    expect(joint).toBeCloseTo(0.00062811, 8);
  });

  it('orders nodes topologically (parents before children)', () => {
    const order = topologicalOrder(alarmNetwork());
    expect(order.indexOf('Burglary')).toBeLessThan(order.indexOf('Alarm'));
    expect(order.indexOf('Earthquake')).toBeLessThan(order.indexOf('Alarm'));
    expect(order.indexOf('Alarm')).toBeLessThan(order.indexOf('JohnCalls'));
    expect(order.indexOf('Alarm')).toBeLessThan(order.indexOf('MaryCalls'));
  });

  it('reports well-formed CPTs as valid', () => {
    expect(validateCpts(alarmNetwork())).toEqual([]);
  });

  it('rejects a 2-node cycle (A -> B -> A) by throwing', () => {
    const cyclic: BayesNetworkModel = {
      nodes: [
        {
          id: 'A',
          name: 'A',
          states: ['true', 'false'],
          parents: ['B'],
          cpt: {
            [cptKey(['true'])]: [0.5, 0.5],
            [cptKey(['false'])]: [0.5, 0.5],
          },
        },
        {
          id: 'B',
          name: 'B',
          states: ['true', 'false'],
          parents: ['A'],
          cpt: {
            [cptKey(['true'])]: [0.5, 0.5],
            [cptKey(['false'])]: [0.5, 0.5],
          },
        },
      ],
    };
    expect(() => topologicalOrder(cyclic)).toThrow(/cycle/i);
    expect(() => enumerationAsk('A', {}, cyclic)).toThrow(/cycle/i);
  });

  it('supports a multi-valued query variable', () => {
    const net: BayesNetworkModel = {
      nodes: [
        {
          id: 'Weather',
          name: 'Weather',
          states: ['sun', 'rain', 'snow'],
          parents: [],
          cpt: { [cptKey([])]: [0.6, 0.3, 0.1] },
        },
      ],
    };
    const m = marginal('Weather', net);
    expect(m.sun).toBeCloseTo(0.6, 10);
    expect(m.rain).toBeCloseTo(0.3, 10);
    expect(m.snow).toBeCloseTo(0.1, 10);
    expect(m.sun + m.rain + m.snow).toBeCloseTo(1, 10);
  });
});
