export abstract class Solver<State, Movement> {
  public seenStates: Map<string, number> = new Map();
  constructor(public debug: boolean = false) {
  }

  abstract possibleMovesIterator(state: State): Generator<Movement[]>;
  abstract isSolution(state: State): boolean;
  abstract applyMovement(state: State, movement: Movement): State;
  abstract undoMovement(state: State, movement: Movement): State;
  abstract formatSolution(state: State): string;

  solve(state: State): State | undefined {
    if (this.debug) {
      const key = this.formatSolution(state);
      const timesSeen = this.seenStates.get(key) || 0;
      if (timesSeen > 0) {
        console.log(`State already seen ${timesSeen} times:`);
        console.log(key);
      }
      this.seenStates.set(key, timesSeen + 1);
      
      if (this.seenStates.size % 10000 === 0) {
        console.log(`movements so far ${this.seenStates.size}`);
      }
    }

    if (this.isSolution(state)) {
      return state;
    }

    let smallestGroup: Movement[] | undefined = undefined;
    for (const movementGroup of this.possibleMovesIterator(state)) {
      const smallestGroupSize = smallestGroup === undefined ? Infinity : smallestGroup.length;
      if (movementGroup.length < smallestGroupSize) {
        smallestGroup = movementGroup;
      }
    }
    
    for (const movement of smallestGroup || []) {
      const nextState = this.applyMovement(state, movement);
      const solution = this.solve(nextState);
      if (solution) {
        return solution;
      }
      this.undoMovement(state, movement);
    }
    return undefined;
  }
}
