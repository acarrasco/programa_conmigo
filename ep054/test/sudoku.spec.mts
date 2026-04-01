import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { Sudoku, type State, type Movement } from "@src/sudoku.mts";

describe("Sudoku", () => {
  const subject = new Sudoku();
  describe("getRow", () => {
    it("should return values for a filled row", () => {
      const row = [1, 2, 3, 4, 5, 6];
      const state: State = {
        board: [
          row,
          Array(6).fill(undefined),
          Array(6).fill(undefined),
          Array(6).fill(undefined),
          Array(6).fill(undefined),
          Array(6).fill(undefined),
        ],
        placedValues: 6,
        regionCols: 3,
        regionRows: 2,
        size: 6,
      };

      const result = subject.getRow(state, 0);
      assert.deepEqual(result, row);
    });

    it("should return values for a partially filled row", () => {
      const row = [1, 2, undefined, 4, undefined, 6];
      const state: State = {
        board: [
          row,
          Array(6).fill(undefined),
          Array(6).fill(undefined),
          Array(6).fill(undefined),
          Array(6).fill(undefined),
          Array(6).fill(undefined),
        ],
        placedValues: 6,
        regionCols: 3,
        regionRows: 2,
        size: 6,
      };

      const result = subject.getRow(state, 0);
      assert.deepEqual(
        result,
        row.filter((x) => x),
      );
    });
  });

  describe("getCol", () => {
    it("should return values for a filled column", () => {
      const state: State = {
        board: [
          [1, undefined, undefined, undefined, undefined, undefined],
          [2, undefined, undefined, undefined, undefined, undefined],
          [3, undefined, undefined, undefined, undefined, undefined],
          [4, undefined, undefined, undefined, undefined, undefined],
          [5, undefined, undefined, undefined, undefined, undefined],
          [6, undefined, undefined, undefined, undefined, undefined],
        ],
        placedValues: 6,
        regionCols: 3,
        regionRows: 2,
        size: 6,
      };

      const result = subject.getCol(state, 0);
      assert.deepEqual(result, [1, 2, 3, 4, 5, 6]);
    });

    it("should return values for a partially filled column", () => {
      const state: State = {
        board: [
          [1, undefined, undefined, undefined, undefined, undefined],
          [undefined, undefined, undefined, undefined, undefined, undefined],
          [3, undefined, undefined, undefined, undefined, undefined],
          [undefined, undefined, undefined, undefined, undefined, undefined],
          [5, undefined, undefined, undefined, undefined, undefined],
          [undefined, undefined, undefined, undefined, undefined, undefined],
        ],
        placedValues: 6,
        regionCols: 3,
        regionRows: 2,
        size: 6,
      };

      const result = subject.getCol(state, 0);
      assert.deepEqual(result, [1, 3, 5]);
    });
  });

  describe("getRegion", () => {
    for (let i = 0; i < 2; i++) {
      for (let j = 0; j < 3; j++) {
        it(`should return values for a filled region ${i} ${j}`, () => {
          const state: State = {
            board: [
              [1, 2, 3, undefined, undefined, undefined],
              [4, 5, 6, undefined, undefined, undefined],
              [3, undefined, undefined, undefined, undefined, undefined],
              [2, undefined, undefined, undefined, undefined, undefined],
              [5, undefined, undefined, 1, 2, undefined],
              [6, undefined, undefined, undefined, 3, 4],
            ],
            placedValues: 6,
            regionCols: 3,
            regionRows: 2,
            size: 6,
          };

          const result = subject.getRegion(state, i, j);
          assert.deepEqual(result, [1, 2, 3, 4, 5, 6]);
        });
      }
    }

    for (let i = 4; i < 6; i++) {
      for (let j = 3; j < 6; j++) {
        it(`should return values for a filled region ${i} ${j}`, () => {
          const state: State = {
            board: [
              [1, 2, 3, undefined, undefined, undefined],
              [4, 5, 6, undefined, undefined, undefined],
              [3, undefined, undefined, undefined, undefined, undefined],
              [2, undefined, undefined, undefined, undefined, undefined],
              [5, undefined, undefined, 1, 2, undefined],
              [6, undefined, undefined, undefined, 3, 4],
            ],
            placedValues: 6,
            regionCols: 3,
            regionRows: 2,
            size: 6,
          };

          const result = subject.getRegion(state, i, j);
          assert.deepEqual(result, [1, 2, 3, 4]);
        });
      }
    }
  });

  describe("getPossibleValuesForCell", () => {
    it("should return all values if no restrictions", () => {
      const state: State = {
        board: [
          [undefined, undefined, undefined, undefined, undefined, undefined],
          [undefined, undefined, undefined, undefined, undefined, undefined],
          [undefined, undefined, undefined, undefined, undefined, undefined],
          [undefined, undefined, undefined, undefined, undefined, undefined],
          [undefined, undefined, undefined, undefined, undefined, undefined],
          [undefined, undefined, undefined, undefined, undefined, undefined],
        ],
        placedValues: 6,
        regionCols: 3,
        regionRows: 2,
        size: 6,
      };

      const result = subject.getPossibleValuesForCell(state, 0, 0);
      assert.deepEqual(result, [1, 2, 3, 4, 5, 6]);
    });

    it("should return some values", () => {
      const state: State = {
        board: [
          [1, undefined, undefined, undefined, undefined, undefined],
          [undefined, undefined, 3, undefined, undefined, undefined],
          [undefined, 4, undefined, undefined, undefined, undefined],
          [undefined, undefined, undefined, undefined, undefined, undefined],
          [undefined, undefined, undefined, undefined, undefined, undefined],
          [undefined, undefined, undefined, undefined, undefined, undefined],
        ],
        placedValues: 6,
        regionCols: 3,
        regionRows: 2,
        size: 6,
      };

      const result = subject.getPossibleValuesForCell(state, 0, 1);
      assert.deepEqual(result, [2, 5, 6]);
    });
  });
});
