import {
  Input,
  type Coordinates,
  type Direction,
  type RestrictionDef,
  type Value,
  type ValueDef,
} from "@src/input.mts";

export type OptionalValue = Value | undefined;
type Solution = OptionalValue[][];

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

export class Tango {
  private candidateSolution: Solution;
  private solutionSize: number;
  private placedValues: number;
  public movementsTried = 0;

  constructor(private input: Input) {
    this.placedValues = input.values.length;
    this.solutionSize = input.rows * input.rows;
    this.candidateSolution = Array(input.rows);
    for (let i = 0; i < input.rows; i++) {
      this.candidateSolution[i] = Array(input.cols).fill(undefined);
    }

    for (const value of input.values) {
      const [[row, col], v] = value;
      this.candidateSolution[row]![col] = v;
    }
  }

  formatSolution(): string {
    const grid: string[][] = Array(this.input.rows);
    for (let i = 0; i < this.input.rows * 2 - 1; i++) {
      grid[i] = Array(this.input.cols);
      for (let j = 0; j < this.input.cols * 2 - 1; j++) {
        grid[i]![j] = ' ';
      }
    }

    for (let i = 0; i < this.candidateSolution.length; i++) {
      for (let j = 0; j < this.candidateSolution[i]!.length; j++) {
        grid[i*2]![j*2] = this.candidateSolution[i]![j] || '.';
      }
    }

    for (const restriction of this.input.restrictions) {
      const [[i0, j0], direction, restrictionType] = restriction;
      const [i1, j1] = applyDirection([i0, j0], direction);
      grid[i0 + i1]![j0 + j1] = restrictionType;
    }

    return grid.map(r => r.join(' ')).join('\n');
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
    valueDef: ValueDef,
    restrictionDef: RestrictionDef,
  ): boolean {
    const [[row, col], value] = valueDef;
    const [restrictionCoordinates, direction, restrictionType] = restrictionDef;
    const [i0, j0] = restrictionCoordinates;
    const [i1, j1] = applyDirection(restrictionCoordinates, direction);

    let other: OptionalValue = undefined;

    if (row === i0 && col === j0) {
      other = this.candidateSolution[i1]![j1];
    } else if (row === i1 && col == j1) {
      other = this.candidateSolution[i0]![j0];
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

  areAllRestrictionsValid(move: ValueDef): boolean {
    for (const restrictionDef of this.input.restrictions) {
      if (!this.isValidRestriction(move, restrictionDef)) {
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

  isValidMove(move: ValueDef): boolean {
    if (!this.areAllRestrictionsValid(move)) {
      return false;
    }
    const [coordinates, value] = move;
    const [row, col] = coordinates;

    const candidateRow = [...this.candidateSolution[row]!];
    candidateRow[col] = value;
    if (!this.isValidSequence(candidateRow)) {
      return false;
    }

    const candidateColumn = Array(this.candidateSolution.length);
    for (let i = 0; i < candidateColumn.length; i++) {
      candidateColumn[i] = this.candidateSolution[i]![col];
    }
    candidateColumn[row] = value;
    if (!this.isValidSequence(candidateColumn)) {
      return false;
    }

    return true;
  }

  placeValue(row: number, col: number, value: Value) {
    this.candidateSolution[row]![col] = value;
    this.placedValues++;
  }

  removeValue(row: number, col: number) {
    this.candidateSolution[row]![col] = undefined;
    this.placedValues--;
  }

  *possibleMovesIterator(): Generator<ValueDef> {
    for (let i = 0; i < this.candidateSolution.length; i++) {
      for (let j = 0; j < this.candidateSolution[i]!.length; j++) {
        if (this.candidateSolution[i]![j] == undefined) {
          for (let v of ["s", "m"] as Value[]) {
            yield [[i, j], v];
          }
        }
      }
    }
  }

  solve(): boolean {
    this.movementsTried++;
    if (this.placedValues == this.solutionSize) {
      return true;
    }
    // find a forced move (the complementary is illegal)
    for (const [[i, j], v] of this.possibleMovesIterator()) {
      const moveAttempt: ValueDef = [[i, j], v];
      const complementaryMove: ValueDef = [[i, j], complementaryValue(v)];
      if (!this.isValidMove(moveAttempt) &&
          this.isValidMove(complementaryMove)) {
        this.placeValue(i, j, complementaryValue(v));
        const solved = this.solve();
        if (!solved) {
          this.removeValue(i, j);
        }
        return solved;
      }
    }

    // guess any non ilegal move
    for (const [[i, j], v] of this.possibleMovesIterator()) {
      const moveAttempt: ValueDef = [[i, j], v];
      if (this.isValidMove(moveAttempt)) {
        this.placeValue(i, j, v);
        const solved = this.solve();
        if (solved) {
          return solved;
        }
        this.removeValue(i, j);
      }
    }
    return false;
  }
}

