const { add } = require('./example');

test('adds two positive numbers', () => {
  expect(add(1, 2)).toBe(3);
});

test('adds a positive and a negative number', () => {
  expect(add(5, -3)).toBe(2);
});

test('adds two negative numbers', () => {
  expect(add(-4, -6)).toBe(-10);
});

test('adds zero and a number', () => {
  expect(add(0, 5)).toBe(5);
});

test('adds a number and zero', () => {
  expect(add(7, 0)).toBe(7);
});