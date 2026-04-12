import fs from "fs";
import z from "zod";
import { Patches, Restriction, type State } from "./patches.mts";


export const Input = z.object({
  rows: z.int().min(1),
  columns: z.int().min(1),
  restrictions: z.array(Restriction),
});

type Input = z.infer<typeof Input>;

function getInitialState(input: Input): State {
  return {
    ...input,
    filled: Array(input.rows)
      .fill(null)
      .map(() => Array(input.columns).fill(false)),
    movements: [],
  };
}

function main() {
  if (process.argv.length != 3) {
    console.log("required argument: filename with the input description");
    return;
  }

  const filename = process.argv[2]!;

  const text = fs.readFileSync(filename).toString();
  const json = JSON.parse(text.toString());
  const input = Input.parse(json);
  const initialState = getInitialState(input);

  const patches = new Patches(true);

  console.log(patches.formatSolution(initialState));

  const solution = patches.solve(initialState);

  console.log(`Movements tried: ${patches.seenStates.size}`);

  if (!solution) {
    console.log("Cannot find solution");
  } else {
    console.log(patches.formatSolution(solution));
  }
}

main();
