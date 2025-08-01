const { add } = require('./example');

describe('add', () => {
  it('should return the sum of two positive numbers', () => {
    expect(add(1, 2)).toBe(3);
  });

  it('should return the sum of two negative numbers', () => {
    expect(add(-1, -2)).toBe(-3);
  });

  it('should return the sum of a positive and a negative number', () => {
    expect(add(1, -2)).toBe(-1);
  });

  it('should return the sum when one of the numbers is zero', () => {
    expect(add(0, 5)).toBe(5);
    expect(add(5, 0)).toBe(5);
  });

  it('should return zero when both numbers are zero', () => {
    expect(add(0, 0)).toBe(0);
  });
});