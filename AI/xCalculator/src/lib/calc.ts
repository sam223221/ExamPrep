/**
 * Safe arithmetic expression evaluator.
 *
 * Framework-free, pure functions — NO React, NO `eval`, NO `Function(...)`.
 * The pipeline is the classic three stages:
 *
 *   tokenize(expr)  ->  Token[]        (lexical analysis)
 *   toRpn(tokens)   ->  Token[]        (shunting-yard: infix -> postfix/RPN)
 *   evalRpn(rpn)    ->  number         (stack-based RPN evaluation)
 *
 * `evaluate(expr)` runs all three. Malformed input and division by zero throw a
 * typed {@link CalcError}; callers (the Calculator UI) catch it and show a
 * friendly inline message instead of crashing.
 *
 * Supported grammar:
 *   - binary operators:  + - * / ^
 *   - unary minus / plus: e.g. `-3`, `+4`, `2 * -3`
 *   - parentheses:        `( ... )`
 *   - numbers:            integers and decimals, e.g. `42`, `3.14`, `.5`
 *
 * Precedence (low -> high):  + -   <   * /   <   ^
 * Associativity:  + - * /  left-associative;  ^  right-associative;  unary minus
 * binds tighter than `^` is NOT assumed — we treat unary minus as having very high
 * precedence so `-2^2` parses as `(-2)^2 = 4` (a deliberate, documented choice for a
 * study calculator where the typed expression reflects exactly what the user sees).
 */

/** Error thrown for any malformed expression or math error (e.g. divide by zero). */
export class CalcError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'CalcError';
    // Restore prototype chain for instanceof checks after transpilation to ES5-ish targets.
    Object.setPrototypeOf(this, CalcError.prototype);
  }
}

/** Token kinds produced by the lexer. */
export type TokenType = 'number' | 'operator' | 'lparen' | 'rparen';

/** A single lexical token. For numbers `value` holds the parsed numeric value. */
export interface Token {
  type: TokenType;
  /** Raw text for operators/parens; the textual number for `number` tokens. */
  text: string;
  /** Present only on `number` tokens. */
  value?: number;
  /** Present only on `operator` tokens: true when the operator is unary (e.g. unary minus). */
  unary?: boolean;
}

const BINARY_OPERATORS = new Set(['+', '-', '*', '/', '^']);

interface OpInfo {
  precedence: number;
  /** 'L' left-associative, 'R' right-associative. */
  assoc: 'L' | 'R';
}

const BINARY_INFO: Record<string, OpInfo> = {
  '+': { precedence: 2, assoc: 'L' },
  '-': { precedence: 2, assoc: 'L' },
  '*': { precedence: 3, assoc: 'L' },
  '/': { precedence: 3, assoc: 'L' },
  '^': { precedence: 4, assoc: 'R' },
};

/** Unary minus/plus precedence — higher than `^` so `-2^2 = (-2)^2`. */
const UNARY_PRECEDENCE = 5;

/**
 * Lexical analysis: turn the raw expression into a flat token list, classifying
 * each `+`/`-` as either binary or unary based on the preceding token.
 *
 * @throws {CalcError} on illegal characters or malformed numbers (e.g. `1.2.3`).
 */
export function tokenize(expr: string): Token[] {
  const tokens: Token[] = [];
  let i = 0;
  const n = expr.length;

  const lastSignificant = (): Token | undefined => tokens[tokens.length - 1];

  while (i < n) {
    const ch = expr[i];

    // Whitespace is insignificant between tokens.
    if (ch === ' ' || ch === '\t' || ch === '\n' || ch === '\r') {
      i += 1;
      continue;
    }

    // Numbers: digits with at most one decimal point. Allow a leading dot (`.5`).
    if ((ch >= '0' && ch <= '9') || ch === '.') {
      let j = i;
      let dotCount = 0;
      while (j < n) {
        const c = expr[j];
        if (c >= '0' && c <= '9') {
          j += 1;
        } else if (c === '.') {
          dotCount += 1;
          if (dotCount > 1) {
            throw new CalcError(`Malformed number near "${expr.slice(i, j + 1)}"`);
          }
          j += 1;
        } else {
          break;
        }
      }
      const raw = expr.slice(i, j);
      if (raw === '.') {
        throw new CalcError('A lone "." is not a number');
      }
      const value = Number(raw);
      if (!Number.isFinite(value)) {
        throw new CalcError(`Malformed number "${raw}"`);
      }
      tokens.push({ type: 'number', text: raw, value });
      i = j;
      continue;
    }

    if (ch === '(') {
      tokens.push({ type: 'lparen', text: '(' });
      i += 1;
      continue;
    }

    if (ch === ')') {
      tokens.push({ type: 'rparen', text: ')' });
      i += 1;
      continue;
    }

    if (ch !== undefined && BINARY_OPERATORS.has(ch)) {
      // Decide unary vs binary for + and -. An operator is unary when it appears
      // at the start, after another operator, or after a left parenthesis.
      const prev = lastSignificant();
      const isUnaryContext =
        prev === undefined || prev.type === 'operator' || prev.type === 'lparen';

      if ((ch === '-' || ch === '+') && isUnaryContext) {
        tokens.push({ type: 'operator', text: ch, unary: true });
      } else {
        tokens.push({ type: 'operator', text: ch, unary: false });
      }
      i += 1;
      continue;
    }

    throw new CalcError(`Unexpected character "${ch}"`);
  }

  return tokens;
}

/**
 * Shunting-yard: convert an infix token stream into Reverse Polish Notation.
 *
 * Unary minus is encoded in the output as an operator token with `unary: true`
 * (a single-operand operator). Unary plus is a no-op and is dropped.
 *
 * @throws {CalcError} on mismatched parentheses.
 */
export function toRpn(tokens: Token[]): Token[] {
  const output: Token[] = [];
  const stack: Token[] = [];

  for (const token of tokens) {
    switch (token.type) {
      case 'number':
        output.push(token);
        break;

      case 'operator': {
        if (token.unary) {
          // Unary plus is identity — drop it entirely.
          if (token.text === '+') break;
          // Unary minus: push with its high precedence; right-associative-like
          // behavior is achieved by only popping operators of strictly higher prec.
          while (stack.length > 0) {
            const top = stack[stack.length - 1]!;
            if (top.type !== 'operator') break;
            const topPrec = top.unary ? UNARY_PRECEDENCE : BINARY_INFO[top.text]!.precedence;
            if (topPrec > UNARY_PRECEDENCE) {
              output.push(stack.pop()!);
            } else {
              break;
            }
          }
          stack.push(token);
          break;
        }

        const info = BINARY_INFO[token.text]!;
        while (stack.length > 0) {
          const top = stack[stack.length - 1]!;
          if (top.type !== 'operator') break;
          const topPrec = top.unary ? UNARY_PRECEDENCE : BINARY_INFO[top.text]!.precedence;
          const shouldPop =
            topPrec > info.precedence ||
            (topPrec === info.precedence && info.assoc === 'L');
          if (shouldPop) {
            output.push(stack.pop()!);
          } else {
            break;
          }
        }
        stack.push(token);
        break;
      }

      case 'lparen':
        stack.push(token);
        break;

      case 'rparen': {
        let foundParen = false;
        while (stack.length > 0) {
          const top = stack.pop()!;
          if (top.type === 'lparen') {
            foundParen = true;
            break;
          }
          output.push(top);
        }
        if (!foundParen) {
          throw new CalcError('Mismatched parentheses: unexpected ")"');
        }
        break;
      }

      default:
        // Exhaustive — TokenType has no other members.
        break;
    }
  }

  while (stack.length > 0) {
    const top = stack.pop()!;
    if (top.type === 'lparen' || top.type === 'rparen') {
      throw new CalcError('Mismatched parentheses: unclosed "("');
    }
    output.push(top);
  }

  return output;
}

/**
 * Evaluate an RPN token stream with a numeric stack.
 *
 * @throws {CalcError} on stack underflow (malformed expression), division by
 * zero, or a non-finite result (e.g. overflow).
 */
export function evalRpn(rpn: Token[]): number {
  const stack: number[] = [];

  for (const token of rpn) {
    if (token.type === 'number') {
      stack.push(token.value as number);
      continue;
    }

    if (token.type === 'operator') {
      if (token.unary) {
        const a = stack.pop();
        if (a === undefined) {
          throw new CalcError('Malformed expression');
        }
        // Only unary minus survives to RPN (unary plus was dropped).
        stack.push(-a);
        continue;
      }

      const b = stack.pop();
      const a = stack.pop();
      if (a === undefined || b === undefined) {
        throw new CalcError('Malformed expression');
      }

      let result: number;
      switch (token.text) {
        case '+':
          result = a + b;
          break;
        case '-':
          result = a - b;
          break;
        case '*':
          result = a * b;
          break;
        case '/':
          if (b === 0) {
            throw new CalcError('Division by zero');
          }
          result = a / b;
          break;
        case '^':
          result = Math.pow(a, b);
          break;
        default:
          throw new CalcError(`Unknown operator "${token.text}"`);
      }

      if (!Number.isFinite(result)) {
        throw new CalcError('Result is not a finite number');
      }
      stack.push(result);
      continue;
    }

    // A paren reaching evaluation means toRpn produced bad output — defensive.
    throw new CalcError('Malformed expression');
  }

  if (stack.length !== 1) {
    throw new CalcError('Malformed expression');
  }
  return stack[0]!;
}

/**
 * Evaluate an arithmetic expression string and return the numeric result.
 *
 * @throws {CalcError} on empty/malformed input, mismatched parens, or math errors.
 *
 * @example
 * evaluate('2+3*4');     // 14
 * evaluate('(2+3)*4');   // 20
 * evaluate('2^3^2');     // 512 (right-associative)
 * evaluate('-3+5');      // 2
 */
export function evaluate(expr: string): number {
  if (typeof expr !== 'string' || expr.trim() === '') {
    throw new CalcError('Empty expression');
  }
  const tokens = tokenize(expr);
  if (tokens.length === 0) {
    throw new CalcError('Empty expression');
  }
  const rpn = toRpn(tokens);
  return evalRpn(rpn);
}
