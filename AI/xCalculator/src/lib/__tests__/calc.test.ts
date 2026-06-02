import { describe, it, expect } from 'vitest';
import { evaluate, tokenize, toRpn, CalcError } from '../calc';

describe('evaluate — precedence & associativity', () => {
  it('respects * over + (2+3*4 = 14)', () => {
    expect(evaluate('2+3*4')).toBe(14);
  });

  it('respects parentheses ((2+3)*4 = 20)', () => {
    expect(evaluate('(2+3)*4')).toBe(20);
  });

  it('evaluates exponentiation (2^10 = 1024)', () => {
    expect(evaluate('2^10')).toBe(1024);
  });

  it('treats ^ as right-associative (2^3^2 = 2^9 = 512)', () => {
    expect(evaluate('2^3^2')).toBe(512);
  });

  it('handles leading unary minus (-3+5 = 2)', () => {
    expect(evaluate('-3+5')).toBe(2);
  });

  it('handles unary minus after an operator (2 * -3 = -6)', () => {
    expect(evaluate('2 * -3')).toBe(-6);
  });

  it('handles unary minus inside parentheses (10 - (-4) = 14)', () => {
    expect(evaluate('10 - (-4)')).toBe(14);
  });

  it('parses -2^2 as (-2)^2 = 4 (documented unary-binds-tighter choice)', () => {
    expect(evaluate('-2^2')).toBe(4);
  });

  it('handles decimals (.5 + 0.25 = 0.75)', () => {
    expect(evaluate('.5 + 0.25')).toBe(0.75);
  });

  it('handles nested parentheses and mixed precedence', () => {
    expect(evaluate('(1 + 2) * (3 + 4) ^ 2')).toBe(147);
  });

  it('ignores surrounding whitespace', () => {
    expect(evaluate('  7  -  2  ')).toBe(5);
  });
});

describe('evaluate — error handling', () => {
  it('throws CalcError on division by zero', () => {
    expect(() => evaluate('1/0')).toThrow(CalcError);
  });

  it('throws CalcError on malformed operator sequence (2+*3)', () => {
    expect(() => evaluate('2+*3')).toThrow(CalcError);
  });

  it('throws CalcError on a trailing operator (2+)', () => {
    expect(() => evaluate('2+')).toThrow(CalcError);
  });

  it('throws CalcError on unmatched closing paren', () => {
    expect(() => evaluate('(1+2))')).toThrow(CalcError);
  });

  it('throws CalcError on unmatched opening paren', () => {
    expect(() => evaluate('(1+2')).toThrow(CalcError);
  });

  it('throws CalcError on an empty expression', () => {
    expect(() => evaluate('   ')).toThrow(CalcError);
  });

  it('throws CalcError on an illegal character', () => {
    expect(() => evaluate('2 & 3')).toThrow(CalcError);
  });

  it('throws CalcError on a malformed number (1.2.3)', () => {
    expect(() => evaluate('1.2.3')).toThrow(CalcError);
  });
});

describe('tokenize / toRpn — internals', () => {
  it('classifies a leading minus as unary', () => {
    const tokens = tokenize('-3');
    expect(tokens[0]).toMatchObject({ type: 'operator', text: '-', unary: true });
  });

  it('classifies the minus in 5-3 as binary', () => {
    const tokens = tokenize('5-3');
    const minus = tokens.find((t) => t.text === '-');
    expect(minus).toMatchObject({ unary: false });
  });

  it('produces RPN for 2+3*4 as [2, 3, 4, *, +]', () => {
    const rpn = toRpn(tokenize('2+3*4'));
    expect(rpn.map((t) => t.text)).toEqual(['2', '3', '4', '*', '+']);
  });
});
