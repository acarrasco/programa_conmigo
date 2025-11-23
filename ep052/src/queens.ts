type Tuple<TItem, TLength extends number> = [TItem, ...TItem[]] & { length: TLength };

function createExactCoverMatrix<S extends number>(puzzle_cells: Tuple<Tuple<string, S>, S>) {
    const size: S = puzzle_cells.length;
    
    const options = size*size;
    const hard_constraints = 3 * size;
    const soft_constraints = 2*(size-2)*(size-2)

    const hard_constraint_headers: Record<string, number> = {};
    const soft_constraint_headers: Record<string, number> = {};
    const option_names: string[] = [];

    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            option_names.push(`cell ${i}, ${j}`);
            const color = puzzle_cells[i]![j]!;
            hard_constraint_headers[`color ${color}`] = (hard_constraint_headers[`color ${color}`] || 0) + 1;
        }
    }

    for (let i = 0; i < size; i++) {
        hard_constraint_headers[`row ${i}`] = size;
    }
    for (let j = 0; j < size; j++) {
        hard_constraint_headers[`col ${j}`] = size;
    }


    for(let i = 0; i < size-1; i++) {
        for(let j = 0; j < size-1; j++) {
            soft_constraint_headers[`diag (${i},${j})-(${i+1},${j+1})`] = 2;
            soft_constraint_headers[`diag (${i},${j+1})-(${i+1},${j})`] = 2;
        }
    }
}