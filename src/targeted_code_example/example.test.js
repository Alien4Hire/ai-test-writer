const { add, subtract, multiply, divide } = require('./example');

describe('Math functions', () => {
  test('add function should return the sum of two numbers', () => {
    expect(add(1, 2)).toBe(3);
    expect(add(-1, -2)).toBe(-3);
    expect(add(-1, 1)).toBe(0);
  });

  test('subtract function should return the difference of two numbers', () => {
    expect(subtract(5, 3)).toBe(2);
    expect(subtract(3, 5)).toBe(-2);
    expect(subtract(-5, -3)).toBe(-2);
  });

  test('multiply function should return the product of two numbers', () => {
    expect(multiply(2, 3)).toBe(6);
    expect(multiply(-2, 3)).toBe(-6);
    expect(multiply(-2, -3)).toBe(6);
  });

  test('divide function should return the quotient of two numbers', () => {
    expect(divide(6, 3)).toBe(2);
    expect(divide(6, -3)).toBe(-2);
    expect(divide(-6, -3)).toBe(2);
  });

  test('divide function should handle division by zero', () => {
    expect(divide(6, 0)).toBe(Infinity);
    expect(divide(-6, 0)).toBe(-Infinity);
    expect(divide(0, 0)).toBeNaN();
  });
});