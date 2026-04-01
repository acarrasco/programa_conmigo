import fs from "fs";

import { Input } from "@src/input.mts";

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
const problem = new Tango(input);
problem.solve();
console.log(`Movements tried: ${problem.movementsTried}`);
console.log(problem.formatSolution());
