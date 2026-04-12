import { Solver } from "./solver.mts";
import z from "zod";

const Shape = z.enum(["S", "V", "H", "?"]);

type Shape = z.infer<typeof Shape>;

export const Restriction = z.object({
  row: z.int().min(0),
  column: z.int().min(0),
  size: z.int().optional(),
  shape: Shape.optional().default("?"),
});

type Restriction = z.infer<typeof Restriction>;

interface Movement {
  restriction: Restriction;
  top: number;
  left: number;
  bottom: number;
  right: number;
}

export interface State {
  restrictions: Restriction[];
  rows: number;
  columns: number;
  filled: boolean[][];
  movements: Movement[];
}

interface Rectangle {
  height: number;
  width: number;
}

function isValidShape(shape: Shape, rectangle: Rectangle): boolean {
  switch (shape) {
    case "?":
      return true;
    case "H":
      return rectangle.width > rectangle.height;
    case "V":
      return rectangle.width < rectangle.height;
    case "S":
      return rectangle.width === rectangle.height;
  }
}

export function getPossibleRectangles(size: number, shape: Shape): Rectangle[] {
  const result: Rectangle[] = [];
  for (let width = 1; width <= size; width++) {
    const height = Math.trunc(size / width);
    if (width * height === size) {
      const rectangle = { width, height };
      if (isValidShape(shape, rectangle)) {
        result.push(rectangle);
      }
    }
  }
  return result;
}

export function isMovementInsideBoard(state: State, movement: Movement) {
  return (
    movement.top >= 0 &&
    movement.left >= 0 &&
    movement.bottom <= state.rows &&
    movement.right <= state.columns
  );
}

export function isInside(row: number, column: number, movement: Movement) {
  return (
    row >= movement.top &&
    row < movement.bottom &&
    column >= movement.left &&
    column < movement.right
  );
}

export function isMovementNonOverlapping(state: State, movement: Movement): boolean {
  for (const restriction of state.restrictions) {
    if (
      restriction !== movement.restriction &&
      isInside(restriction.row, restriction.column, movement)
    ) {
      return false;
    }
  }

  for (let i = movement.top; i < movement.bottom; i++) {
    for (let j = movement.left; j < movement.right; j++) {
      if (state.filled[i]![j]) {
        return false;
      }
    }
  }
  return true;
}

export function isValidMovement(state: State, movement: Movement): boolean {
  return (
    isMovementInsideBoard(state, movement) &&
    isMovementNonOverlapping(state, movement)
  );
}

export function getPossibleSizes(state: State, restriction: Restriction): number[] {
  if (restriction.size) {
    return [restriction.size];
  }
  const result: number[] = [];
  const maxSize = state.rows * state.columns;

  for (let size = 2; size <= maxSize; size++) {
    result.push(size);
  }
  return result;
}

export function getPossibleMovementsForRestriction(
  state: State,
  restriction: Restriction,
): Movement[] {
  const result: Movement[] = [];
  for (const size of getPossibleSizes(state, restriction)) {
    for (const rectangle of getPossibleRectangles(size, restriction.shape)) {
      for (let di = 0; di < rectangle.height; di++) {
        for (let dj = 0; dj < rectangle.width; dj++) {
          const top = restriction.row - di;
          const bottom = top + rectangle.height;
          const left = restriction.column - dj;
          const right = left + rectangle.width;
          const movement: Movement = {
            top,
            bottom,
            left,
            right,
            restriction,
          };
          if (isValidMovement(state, movement)) {
            result.push(movement);
          }
        }
      }
    }
  }

  return result;
}

export class Patches extends Solver<State, Movement> {
  *possibleMovesIterator(state: State): Generator<Movement[], any, any> {
    const fullfiledRestrictions = new Set<Restriction>(
      state.movements.map((m) => m.restriction),
    );
    for (const restriction of state.restrictions) {
      if (!fullfiledRestrictions.has(restriction)) {
        yield getPossibleMovementsForRestriction(state, restriction);
      }
    }
  }
  isSolution(state: State): boolean {
    if (state.restrictions.length !== state.movements.length) {
      return false
    };
    for (let i = 0; i < state.rows; i++) {
      for (let j = 0; j < state.columns; j++) {
        if (!state.filled[i]![j]) {
          return false;
        }
      }
    }
    return true;
  }
  applyMovement(state: State, movement: Movement): State {
    state.movements.push(movement);
    for (let i = movement.top; i < movement.bottom; i++) {
      for (let j = movement.left; j < movement.right; j++) {
        state.filled[i]![j] = true;
      }
    }
    return state;
  }
  undoMovement(state: State, movement: Movement): State {
    const lastMovement = state.movements.pop();
    console.assert(lastMovement === movement);
    for (let i = movement.top; i < movement.bottom; i++) {
      for (let j = movement.left; j < movement.right; j++) {
        state.filled[i]![j] = false;
      }
    }
    return state;
  }
  formatSolution(state: State): string {
    const board: string[][] = Array(state.rows)
      .fill(null)
      .map(() => Array(state.columns).fill(" . "));

    for (const restriction of state.restrictions) {
      const { row, column, size, shape } = restriction;
      board[row]![column] = `${shape}${size ?? '?'}`.padEnd(3);
    }

    for (
      let movementIdx = 0;
      movementIdx < state.movements.length;
      movementIdx++
    ) {
      const movementSymbol =
        " " + String.fromCharCode("A".charCodeAt(0) + movementIdx) + " ";
      const movement = state.movements[movementIdx]!;

      for (let i = movement.top; i < movement.bottom; i++) {
        for (let j = movement.left; j < movement.right; j++) {
          board[i]![j] = movementSymbol;
        }
      }
    }

    const rows = board.map((row) => row.join(" "));
    return rows.join("\n");
  }
}
