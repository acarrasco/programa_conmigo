import fs from "fs";

import { Input } from "@src/input_tango.mjs";

import { Tango } from "@src/tango.mts";

async function parseInput(filename: string): Promise<Input> {
  const buffer = await fs.promises.readFile(filename);
  const text = buffer.toString();
  const json = JSON.parse(text.toString());
  return Input.parse(json);
}

if (process.argv.length != 3) {
  console.log("required argument: filename with the input description");
}


const filename = process.argv[2];
const input = await parseInput(filename!);
const initialState = Tango.initialState(input);
const problem = new Tango(true);
const solution = problem.solve(initialState);
if (!solution) {
  console.log("Cannot find solution");
} else {
  console.log(`Movements tried: ${problem.seenStates.size}`)
  console.log(problem.formatSolution(solution));
}
