import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { Tango, type OptionalValue,  } from "@src/tango.mjs";
import {type RestrictionDef, type Value, type ValueDef } from '@src/input.mjs';

describe("tango", () => {
  const instance = new Tango({
    rows: 0,
    cols: 0,
    values: [],
    restrictions: [],
  });

  describe("isNoMoreThanTwoRepeatedRuleValid", () => {
    for (const value of ["s", "m"] as OptionalValue[]) {
      it(`should return false with three consecutive ${value} at the beginning`, () => {
        const result = instance.isNoMoreThanTwoRepeatedRuleValid([
          value,
          value,
          value,
          undefined,
          undefined,
          undefined,
        ]);
        assert.equal(result, false);
      });

      it(`should return false with three consecutive ${value} at the end`, () => {
        const result = instance.isNoMoreThanTwoRepeatedRuleValid([
          undefined,
          undefined,
          undefined,
          value,
          value,
          value,
        ]);
        assert.equal(result, false);
      });

      it("should return true with all undefined", () => {
        const result = instance.isNoMoreThanTwoRepeatedRuleValid([
          undefined,
          undefined,
          undefined,
          undefined,
          undefined,
          undefined,
        ]);

        assert.equal(result, true);
      });

      it(`should return false with 's', 's', 'm', 'm', 'm', 's'`, () => {
        const result = instance.isNoMoreThanTwoRepeatedRuleValid([
          's',
          's',
          'm',
          'm',
          'm',
          's',
        ]);

        assert.equal(result, false);
      });

      it("should return true with all interleaved", () => {
        const result = instance.isNoMoreThanTwoRepeatedRuleValid([
          "s",
          "m",
          "s",
          "m",
          "s",
          "m",
        ]);

        assert.equal(result, true);
      });

      it("should return true with pairs interleaved", () => {
        const result = instance.isNoMoreThanTwoRepeatedRuleValid([
          "m",
          "m",
          "s",
          "s",
          "m",
          "s",
        ]);

        assert.equal(result, true);
      });
    }
  });

  describe("isSameAmountRuleValid", () => {
    for (const value of ["s", "m"] as OptionalValue[]) {
      it(`should return false with more than half ${value}`, () => {
        const result = instance.isSameAmountRuleValid([
          value,
          value,
          undefined,
          value,
          value,
          undefined,
        ]);
      });

      it(`should return true with half or less ${value}`, () => {
        const result = instance.isSameAmountRuleValid([
          value,
          undefined,
          undefined,
          value,
          value,
          undefined,
        ]);
      });
    }

    it("should return true with all undefined", () => {
      const result = instance.isSameAmountRuleValid([
        undefined,
        undefined,
        undefined,
        undefined,
        undefined,
        undefined,
      ]);
    });
  });

  describe('validateRestriction', () => {
    describe('different', () => {
      for(const [value, other, expected] of [
        ['s', undefined, true],
        ['m', undefined, true],
        ['s', 'm', true],
        ['m', 's', true],
        ['s', 's', false],
        ['m', 'm', false],
      ] as [Value, Value | undefined, boolean][]) {
        it(`should return ${expected} if the movement is ${value} and the other is ${other}`, () => {
          const movement: ValueDef = [[0, 1], value];
          const restriction: RestrictionDef = [[0, 0], 'R', 'x'];
          const restrictionInstance: Tango = new Tango({
            cols: 6,
            rows: 6,
            restrictions: [restriction],
            values: [],
          });

          if (other) {
            restrictionInstance.placeValue(0, 0, other);
          }

          const result = restrictionInstance.isValidRestriction(movement, restriction);
          assert.equal(result, expected);
        });
      }
    });

    describe('equal', () => {
            for(const [value, other, expected] of [
        ['s', undefined, true],
        ['m', undefined, true],
        ['s', 'm', false],
        ['m', 's', false],
        ['s', 's', true],
        ['m', 'm', true],
      ] as [Value, Value | undefined, boolean][]) {
        it(`should return ${expected} if the movement is ${value} and the other is ${other}`, () => {
          const movement: ValueDef = [[0, 1], value];
          const restriction: RestrictionDef = [[0, 0], 'R', '='];
          const restrictionInstance: Tango = new Tango({
            cols: 6,
            rows: 6,
            restrictions: [restriction],
            values: [],
          });

          if (other) {
            restrictionInstance.placeValue(0, 0, other);
          }

          const result = restrictionInstance.isValidRestriction(movement, restriction);
          assert.equal(result, expected);
        });
      }
    })
  });

});
