import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { getPossibleRectangles, Patches } from "@src/patches.mts";

describe("Patches", () => {
  const subject = new Patches();

  describe("getPossibleRectangles", () => {
    it("should generate a square of size 2x2", () => {
      const result = getPossibleRectangles(4, "S");
      assert.deepEqual(result, [
        {
          width: 2,
          height: 2,
        },
      ]);
    });

    it("should generate a rectangle of size 1x4", () => {
      const result = getPossibleRectangles(4, "H");
      assert.deepEqual(result, [
        {
          width: 4,
          height: 1,
        },
      ]);
    });

    it("should generate a rectangle of size 4x1", () => {
      const result = getPossibleRectangles(4, "V");
      assert.deepEqual(result, [
        {
          width: 1,
          height: 4,
        },
      ]);
    });

    it("should generate all rectangles of area 4", () => {
      const result = getPossibleRectangles(4, "?");
      assert.deepEqual(result, [
        {
          width: 1,
          height: 4,
        },
        {
          width: 2,
          height: 2,
        },
        {
          width: 4,
          height: 1,
        },
      ]);
    });
  });

  describe("isMovementInsideBoard", () => {
    
  });
});
