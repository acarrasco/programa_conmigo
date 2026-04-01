import { Solver } from "@src/solver.mts";

type Board = (number | undefined)[][];

export interface State {
  board: Board;
  regionRows: number;
  regionCols: number;
  size: number;
  placedValues: number;
}

interface Movement {
  row: number;
  col: number;
  value: number;
}

export class Sudoku extends Solver<State, Movement> {

  formatSolution(state: State): string {
    const padRow = (i: number) => (i + 1) % state.regionRows === 0 && '\n' || '';
    const padCol = (j: number) => (j + 1) % state.regionCols === 0 && ' ' || '';
    return state.board.map((row, i) => row.map((v, j) => (v || '.') + padCol(j)).join(' ') + padRow(i)).join('\n');
  }

  getRow(state: State, row: number): number[] {
    const result: number[] = [];
    for (let col = 0; col < state.size; col++) {
      if (state.board[row]![col] !== undefined) {
        result.push(state.board[row]![col]!);
      }
    }
    return result;
  }

  getCol(state: State, col: number): number[] {
    const result: number[] = [];
    for (let row = 0; row < state.size; row++) {
      if (state.board[row]![col] !== undefined) {
        result.push(state.board[row]![col]!);
      }
    }
    return result;
  }

  getRegion(state: State, row: number, col: number): number[] {
    const result: number[] = [];
    const regionMinRow = row - (row % state.regionRows);
    const regionMinCol = col - (col % state.regionCols);
    const regionMaxRow = regionMinRow + state.regionRows;
    const regionMaxCol = regionMinCol + state.regionCols;

    for (let i = regionMinRow; i < regionMaxRow; i++) {
      for (let j = regionMinCol; j < regionMaxCol; j++) {
        const value = state.board[i]![j];
        if (value !== undefined) {
          result.push(value);
        }
      }
    }
    return result;
  }

  getPossibleValuesForCell(state: State, row: number, col: number): number[] {
    const isUsed = Array(state.size + 1).fill(false);
    for (const value of this.getRow(state, row)) {
      isUsed[value] = true;
    }
    for (const value of this.getCol(state, col)) {
      isUsed[value] = true;
    }
    for (const value of this.getRegion(state, row, col)) {
      isUsed[value] = true;
    }
    const result: number[] = [];

    for (let value = 1; value < isUsed.length; value++) {
      if (!isUsed[value]) {
        result.push(value);
      }
    }
    return result;
  }

  *possibleMovesIterator(state: State): Generator<Movement[]> {
    for (let row = 0; row < state.size; row++) {
      for (let col = 0; col < state.size; col++) {
        if (state.board[row]![col] === undefined) {
          const group: Movement[] = [];
          for (const value of this.getPossibleValuesForCell(state, row, col)) {
            group.push({
              row,
              col,
              value,
            });
          }
          yield group;
        }
      }
    }
  }

  isSolution(state: State): boolean {
    return state.placedValues === state.size * state.size;
  }

  applyMovement(state: State, movement: Movement): State {
    const { row, col, value } = movement;
    state.board[row]![col] = value;
    state.placedValues++;
    return state;
  }

  undoMovement(state: State, movement: Movement): State {
    const { row, col } = movement;
    state.board[row]![col] = undefined;
    state.placedValues--;
    return state;
  }
}
