import fs from 'fs';
import { getInitialState, Queens } from "./queens.mts";

async function readFileAsWordArray(filename: string): Promise<string[][]> {
    try {
        const data = await fs.promises.readFile(filename, 'utf8');
        const rows = data.split(/\n/);
        return rows.map(row => row.trim().split(/\s+/));
    } catch (error) {
        console.error(`Error reading file ${filename}:`, error);
        throw new Error('File could not be read or does not exist');
    }
}

if (process.argv.length < 3) {
    throw new Error('missing input file argument');
}

const grid = await readFileAsWordArray(process.argv[2]!);
const initialState = getInitialState(grid);
// console.log(problem.exact_cover_constraints);
const problem = new Queens(true);
const solution = problem.solve(initialState);
if (!solution) {
  console.log("Cannot find solution");
} else {
  console.log(`Movements tried: ${problem.seenStates.size}`)
  console.log(problem.formatSolution(solution));
}
