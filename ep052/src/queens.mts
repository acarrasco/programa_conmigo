import fs from 'fs';

import { SparseBooleanMatrix } from './sparse_boolean_matrix.mjs';


function optionName(i: number, j: number): string {
    return `cell (${i},${j})`;
}

function rowConstraintName(i: number): string {
    return `row ${i}`;
}

function colConstraintName(j: number): string {
    return `col ${j}`;
}

function regionConstraintName(color: string): string {
    return `region ${color}`;
}

function diagConstraintName(i0: number, j0: number, i1: number, j1: number): string {
    return `diag (${i0},${j0})-(${i1},${j1})`;
}

function getDiagonalConstraints(size: number, i: number, j: number): string[] {
    const result = [];
    if (i > 0 && j > 0) {
        result.push(diagConstraintName(i-1, j-1, i, j));
    }
    if (i > 0 && j < size - 1) {
        result.push(diagConstraintName(i-1, j+1, i, j));
    }
    if (i < size - 1 && j < size - 1) {
        result.push(diagConstraintName(i, j, i+1, j+1));
    }
    if (i < size - 1 && j > 0) {
        result.push(diagConstraintName(i, j, i+1, j-1));
    }
    return result;
}

interface Problem<Option extends string, Constraint extends string> {
    exact_cover_constraints: SparseBooleanMatrix<Option, Constraint>;
    options: Option[];
    hard_constraints: Constraint[];
}


function makeExactCoverQueensProblem(grid: string[][]): Problem<string, string> {
    const size = grid.length;

    const options_headers: string[] = [];
    const hard_constraints_headers : string[] = [];
    const soft_constraints_headers : string[] = [];

    const color_counts: Record<string, number> = {};

    // define options (rows)

    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            options_headers.push(optionName(i, j));
            const color = grid[i]![j]!;
            color_counts[color] = (color_counts[color] || 0) + 1;
        }
    }

    // define constraints (columns)

    for (let i = 0; i < size; i++) {
        const name = `row ${i}`;
        hard_constraints_headers.push(name);
    }

    for (let j = 0; j < size; j++) {
        hard_constraints_headers.push(colConstraintName(j))
    }

    for (const color in color_counts) {
        hard_constraints_headers.push(regionConstraintName(color));
    }

    for (let i = 0; i < size-1; i++) {
        for (let j = 0; j < size-1; j++) {;
            soft_constraints_headers.push(diagConstraintName(i, j, i+1, j+1));
            soft_constraints_headers.push(diagConstraintName(i, j+1, i+1, j));
        }
    }

    // create matrix

    const matrix = new SparseBooleanMatrix(options_headers, [...hard_constraints_headers, ...soft_constraints_headers]);

    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const color = grid[i]![j]!;
            const r = optionName(i, j);
            matrix.setElement(r, rowConstraintName(i));
            matrix.setElement(r, colConstraintName(j));
            matrix.setElement(r, regionConstraintName(color));
            for (const d of getDiagonalConstraints(size, i, j)) {
                matrix.setElement(r, d);
            }
        }
    }

    return {
        exact_cover_constraints: matrix,
        options: options_headers,
        hard_constraints: hard_constraints_headers,
    };
}


type UndoItem<Option extends string, Constraint extends string> = {
    type: 'option',
    option_index: number,
} | {
    type: 'row',
    row_header: Option;
    columns: Set<Constraint>;
} | {
    type: 'column',
    column_header: Constraint;
    rows: Set<Option>;
};

function isSolvable<Option extends string, Constraint extends string>(
    matrix: SparseBooleanMatrix<Option, Constraint>,
    hard_constraints: Set<Constraint>): boolean {

    const columns = matrix.getColumns();
    for (const col of hard_constraints.keys()) {
        if (columns[col] && columns[col].size === 0) {
            return false;
        }
    }
    return true;
}

function solve<Option extends string, Constraint extends string>(problem: Problem<Option, Constraint>): Option[] {

    const hard_constraints = new Set<Constraint>(problem.hard_constraints);
    const missing_constraints = new Set<Constraint>(problem.hard_constraints);
    const undo_stack: UndoItem<Option, Constraint>[] = [];
    const matrix = problem.exact_cover_constraints;
    const options = problem.options;

    undo_stack.push({
        type: 'option',
        option_index: -1,
    });

    while (missing_constraints.size > 0 && undo_stack.length > 0) {
        let undo_item: UndoItem<Option, Constraint> | undefined;
        do {
            undo_item = undo_stack.pop();
            if (!undo_item) {
                throw Error('cannot undo');
            }

            if (undo_item.type === 'row') {
                matrix.addRow(undo_item.row_header, undo_item.columns);
            } else if (undo_item.type === 'column') {
                const c = undo_item.column_header;
                if (hard_constraints.has(c)) {
                    missing_constraints.add(c)
                }
                matrix.addColumn(c, undo_item.rows);
            }
        } while(undo_item.type !== 'option');

        let next_option = undo_item.option_index + 1;
        while (next_option < options.length && isSolvable(matrix, hard_constraints)) {
            while (next_option < options.length && !matrix.hasRow(options[next_option]!)) {
                next_option++;
            }
        
            const option = options[next_option];
            if (option) {
                undo_stack.push({
                    type: 'option',
                    option_index: next_option,
                });
                const columns = matrix.deleteRow(option);
                undo_stack.push({
                    type: 'row',
                    row_header: option,
                    columns,
                });
                for (const c of columns) {
                    const rows = matrix.deleteColumn(c);
                    missing_constraints.delete(c);
                    undo_stack.push({
                        type: 'column',
                        column_header: c,
                        rows,
                    });
                    for (const r of rows) {
                        undo_stack.push({
                            type: 'row',
                            row_header: r,
                            columns: matrix.deleteRow(r),
                        });
                    }
                }
            }
        }
    }

    console.log('finish');

    const solution = undo_stack.filter(item => item.type === 'option').map(item => options[item.option_index]!);
    return solution;
}

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
const problem = makeExactCoverQueensProblem(grid);
// console.log(problem.exact_cover_constraints);
const solution = solve(problem);

console.log(solution.join('\n'));