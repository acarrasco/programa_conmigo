import {
  Input,
  type Coordinates,
  type Direction,
  type RestrictionDef,
  type Value,
  type ValueDef,
} from "@src/input_tango.mjs";

import { Solver } from "@src/solver.mts";

export type OptionalValue = Value | undefined;

interface State {
  board: OptionalValue[][];
  placedValues: number;
  solutionSize: number;
  restrictions: RestrictionDef[];
}

function applyDirection(
  coordinates: Coordinates,
  direction: Direction,
): Coordinates {
  const [row, col] = coordinates;
  switch (direction) {
    case "R":
      return [row, col + 1];
    case "D":
      return [row + 1, col];
    case "L":
      return [row, col - 1];
    case "U":
      return [row - 1, col];
  }
}

function complementaryValue(value: Value): Value {
  switch (value) {
    case "s":
      return "m";
    case "m":
      return "s";
  }
}

export class Tango extends Solver<State, ValueDef> {
  static initialState(input: Input): State {
    const placedValues = input.values.length;
    const solutionSize = input.rows * input.rows;
    const board = Array(input.rows);
    const restrictions = input.restrictions;

    for (let i = 0; i < input.rows; i++) {
      board[i] = Array(input.cols).fill(undefined);
    }

    for (const value of input.values) {
      const [[row, col], v] = value;
      board[row]![col] = v;
    }
    return {
      board,
      placedValues,
      solutionSize,
      restrictions,
    };
  }

  formatSolution(state: State): string {
    const size = state.board.length;
    const grid: string[][] = Array(size);
    for (let i = 0; i < size * 2 - 1; i++) {
      grid[i] = Array(size);
      for (let j = 0; j < size * 2 - 1; j++) {
        if (i % 2 && j % 2) {
          grid[i]![j] = "+";
        } else if (i % 2) {
          grid[i]![j] = "-";
        } else if (j % 2) {
          grid[i]![j] = "|";
        } else {
          grid[i]![j] = " ";
        }
      }
    }

    for (let i = 0; i < state.board.length; i++) {
      for (let j = 0; j < state.board[i]!.length; j++) {
        grid[i * 2]![j * 2] = state.board[i]![j] || ".";
      }
    }

    for (const restriction of state.restrictions) {
      const [[i0, j0], direction, restrictionType] = restriction;
      const [i1, j1] = applyDirection([i0, j0], direction);
      grid[i0 + i1]![j0 + j1] = restrictionType;
    }

    return grid.map((r) => r.join(" ")).join("\n");
  }

  isNoMoreThanTwoRepeatedRuleValid(sequence: OptionalValue[]): boolean {
    for (let i = 0; i < sequence.length - 2; i++) {
      const [a, b, c] = sequence.slice(i, i + 3);
      if (a !== undefined && a == b && b == c) {
        return false;
      }
    }
    return true;
  }

  isSameAmountRuleValid(sequence: OptionalValue[]): boolean {
    const max = sequence.length / 2;
    let moons = 0;
    let suns = 0;
    for (const value of sequence) {
      switch (value) {
        case "m":
          moons++;
          break;
        case "s":
          suns++;
          break;
      }
    }
    return moons <= max && suns <= max;
  }

  isValidRestriction(
    state: State,
    valueDef: ValueDef,
    restrictionDef: RestrictionDef,
  ): boolean {
    const [[row, col], value] = valueDef;
    const [restrictionCoordinates, direction, restrictionType] = restrictionDef;
    const [i0, j0] = restrictionCoordinates;
    const [i1, j1] = applyDirection(restrictionCoordinates, direction);

    let other: OptionalValue = undefined;

    if (row === i0 && col === j0) {
      other = state.board[i1]![j1];
    } else if (row === i1 && col == j1) {
      other = state.board[i0]![j0];
    }

    if (!other) {
      return true;
    }

    switch (restrictionType) {
      case "=":
        return value === other;
      case "x":
        return value !== other;
    }
  }

  areAllRestrictionsValid(state: State, move: ValueDef): boolean {
    for (const restrictionDef of state.restrictions) {
      if (!this.isValidRestriction(state, move, restrictionDef)) {
        return false;
      }
    }
    return true;
  }

  isValidSequence(sequence: OptionalValue[]): boolean {
    return (
      this.isSameAmountRuleValid(sequence) &&
      this.isNoMoreThanTwoRepeatedRuleValid(sequence)
    );
  }

  isValidMove(state: State, move: ValueDef): boolean {
    if (!this.areAllRestrictionsValid(state, move)) {
      return false;
    }
    const [coordinates, value] = move;
    const [row, col] = coordinates;

    const candidateRow = [...state.board[row]!];
    candidateRow[col] = value;
    if (!this.isValidSequence(candidateRow)) {
      return false;
    }

    const candidateColumn = Array(state.board.length);
    for (let i = 0; i < candidateColumn.length; i++) {
      candidateColumn[i] = state.board[i]![col];
    }
    candidateColumn[row] = value;
    if (!this.isValidSequence(candidateColumn)) {
      return false;
    }

    return true;
  }

  isSolution(state: State): boolean {
    return state.placedValues === state.solutionSize;
  }
  
  applyMovement(state: State, movement: ValueDef): State {
    const [[row, col], value] = movement;
    state.board[row]![col] = value;
    state.placedValues++;
    return state;
  }

  undoMovement(state: State, movement: ValueDef): State {
    const [[row, col], _value] = movement;
    state.board[row]![col] = undefined;
    state.placedValues--;
    return state;
  }


  *possibleMovesIterator(state: State): Generator<ValueDef[]> {
    for (let i = 0; i < state.board.length; i++) {
      for (let j = 0; j < state.board[i]!.length; j++) {
        if (state.board[i]![j] == undefined) {
          const group: ValueDef[] = [];
          for (let v of ["s", "m"] as Value[]) {
            const candidateMove: ValueDef = [[i, j], v];
            if (this.isValidMove(state, candidateMove)) {
              group.push(candidateMove);
            }
          }
          yield group;
        }
      }
    }
  }
}
