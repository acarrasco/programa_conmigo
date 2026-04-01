import fs from "fs";

import { Sudoku, type State } from "@src/sudoku.mts";

interface Arguments {
  filename: string;
  regionRows: number;
  regionCols: number;
}

function parseArguments(): Arguments {
  const args = process.argv.slice(2);

  if (args.length !== 3) {
    console.error(
      "Usage: node sudoku.js <region_rows> <region_columns> <input_file>",
    );
    process.exit(1);
  }

  const regionRows = parseInt(args[0]!);
  const regionCols = parseInt(args[1]!);
  const filename = args[2];

  if (
    isNaN(regionRows) ||
    isNaN(regionCols) ||
    regionRows <= 0 ||
    regionCols <= 0
  ) {
    console.error(
      "Error: region_rows and region_columns must be positive integers",
    );
    process.exit(1);
  }

  if (filename === undefined) {
    console.error("Error: file name must be defined");
    process.exit(1);
  }

  return {
    filename,
    regionRows,
    regionCols,
  };
}

async function getInitialState(args: Arguments): Promise<State> {
  const {filename, regionRows, regionCols } = args;
  const size = regionRows * regionCols;
  const buffer = await fs.promises.readFile(filename);
  const text = buffer.toString();
  const board: (number|undefined)[][] = Array(size).fill(undefined).map(
    () => Array(size).fill(undefined)
  );

  // Parse initial values from input
  const numbers = text
    .trim()
    .split(/\s+/)
    .map((num) => parseInt(num));


  if (numbers.length !== size * size) {
    console.error(
      `Error: Expected ${size * size} numbers, got ${numbers.length}`,
    );
    process.exit(1);
  }

  let placedValues = 0;
  for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] !== 0) {
      // 0 represents empty cell
      const row = Math.floor(i / size);
      const col = i % size;
      board[row]![col] = numbers[i];
      placedValues++;
    }
  }

  return {
    board,
    placedValues,
    regionRows,
    regionCols,
    size
  }
}

const initialState = await getInitialState(parseArguments());
const problem = new Sudoku(true);
const solution = problem.solve(initialState);
if (!solution) {
  console.log("Cannot find solution");
} else {
  console.log(`Movements tried: ${problem.seenStates.size}`)
  console.log(problem.formatSolution(solution));
}
