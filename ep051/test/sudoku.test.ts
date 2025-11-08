
import { expect } from 'chai';
import { SudokuBoard } from '../src/sudoku';

describe('SudokuBoard', () => {
  it('should be instantiable', () => {
  const board = new SudokuBoard(3, 3, {});
  expect(board).to.be.instanceOf(SudokuBoard);
  });

  it('should generate row neighbors correctly', () => {
    const board = new SudokuBoard(3, 3, {});
    const row0 = Array.from(board.row_neighbor_indices(0, 0));
    expect(row0).to.deep.equal([1, 2, 3, 4, 5, 6, 7, 8]);
    const row1 = Array.from(board.row_neighbor_indices(1, 1));
    expect(row1).to.deep.equal([9, 11, 12, 13, 14, 15, 16, 17]);
  });

  it('should generate column neighbors correctly', () => {
    const board = new SudokuBoard(3, 3, {});
    const col0 = Array.from(board.column_neighbor_indices(0, 0));
    expect(col0).to.deep.equal([9, 18, 27, 36, 45, 54, 63, 72]);
    const col1 = Array.from(board.column_neighbor_indices(2, 1));
    expect(col1).to.deep.equal([1, 10, 28, 37, 46, 55, 64, 73]);
  });

  it('should generate region neighbors correctly', () => {
    const board = new SudokuBoard(3, 3, {});
    const region0 = Array.from(board.region_neighbor_indices(0, 0));
    expect(region0).to.deep.equal([1, 2, 9, 10, 11, 18, 19, 20]);
    const region1 = Array.from(board.region_neighbor_indices(4, 4));
    expect(region1).to.deep.equal([30, 31, 32, 39, 41, 48, 49, 50]);
  });

});
