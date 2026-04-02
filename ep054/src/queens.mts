import fs from 'fs';

import { SparseBooleanMatrix } from './sparse_boolean_matrix.mjs';
import { Solver } from './solver.mts';
import { assert } from 'console';


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


export function getInitialState(grid: string[][]): State<string, string> {
    const size = grid.length;

    const optionHeaders: string[] = [];
    const hardConstraints : string[] = [];
    const softConstraints : string[] = [];

    const colorCounts: Record<string, number> = {};

    // define options (rows)

    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            optionHeaders.push(optionName(i, j));
            const color = grid[i]![j]!;
            colorCounts[color] = (colorCounts[color] || 0) + 1;
        }
    }

    // define constraints (columns)

    for (let i = 0; i < size; i++) {
        hardConstraints.push(rowConstraintName(i));
    }

    for (let j = 0; j < size; j++) {
        hardConstraints.push(colConstraintName(j))
    }

    for (const color in colorCounts) {
        hardConstraints.push(regionConstraintName(color));
    }

    for (let i = 0; i < size-1; i++) {
        for (let j = 0; j < size-1; j++) {;
            softConstraints.push(diagConstraintName(i, j, i+1, j+1));
            softConstraints.push(diagConstraintName(i, j+1, i+1, j));
        }
    }

    // create matrix

    const matrix = new SparseBooleanMatrix(optionHeaders, [...hardConstraints, ...softConstraints]);

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
        matrix,
        hardConstraints: new Set(hardConstraints),
        missingConstraints: new Set(hardConstraints),
        selectedOptions: [],
    };
}


type UndoItem<Option extends string, Constraint extends string> = {
    type: 'row',
    rowHeader: Option;
    columns: Set<Constraint>;
} | {
    type: 'column',
    columnHeader: Constraint;
    rows: Set<Option>;
};


interface State<Option extends string, Constraint extends string> {
    matrix: SparseBooleanMatrix<Option, Constraint>;
    hardConstraints: Set<Constraint>;
    missingConstraints: Set<Constraint>;
    selectedOptions: Option[];
}

interface Movement<Option extends string, Constraint extends string> {
    option: Option;
    undo?: UndoItem<Option, Constraint>[];
}

export class Queens<O extends string, C extends string> extends Solver<State<O, C>, Movement<O, C>> {
    *possibleMovesIterator(state: State<O, C>): Generator<Movement<O, C>[]> {
        const columns = state.matrix.getColumns();
        for (const constraint of state.missingConstraints) {
            const column = columns[constraint];
            if (!column) {
                yield [];
            } else {
                const group: Movement<O, C>[] = column.keys().map(option => {return { option }}).toArray();
                yield group;
            }            
        }
    }

    isSolution(state: State<O, C>): boolean {
        return state.missingConstraints.size === 0;
    }

    applyMovement(state: State<O, C>, movement: Movement<O, C>): State<O, C> {
        const undo: UndoItem<O, C>[] = [];
        const columns = state.matrix.deleteRow(movement.option);
        undo.push({
            type: 'row',
            rowHeader: movement.option,
            columns,
        });
        for (const columnHeader of columns) {
            const rows = state.matrix.deleteColumn(columnHeader);
            undo.push({
                type: 'column',
                columnHeader,
                rows
            });
            for (const rowHeader of rows) {
                undo.push({
                        type: 'row',
                        rowHeader,
                        columns: state.matrix.deleteRow(rowHeader)
                    }
                );
            }

            state.missingConstraints.delete(columnHeader);
        }
        
        movement.undo = undo;
        state.selectedOptions.push(movement.option);
        return state;
    }

    undoMovement(state: State<O, C>, movement: Movement<O, C>): State<O, C> {
        while (movement.undo?.length) {
            const undoItem = movement.undo.pop();
            switch (undoItem?.type) {
                case 'row':
                    const {rowHeader, columns} = undoItem;
                    state.matrix.addRow(rowHeader, columns);
                    break;
                case 'column':
                    const {columnHeader, rows} = undoItem;
                    state.matrix.addColumn(columnHeader, rows);
                    if (state.hardConstraints.has(columnHeader)) {
                       state.missingConstraints.add(columnHeader);
                    }
                    break;
            }
        }
        const option = state.selectedOptions.pop();
        assert(option === movement.option);
        return state;
    }

    formatSolution(state: State<O, C>): string {
        const sorted = state.selectedOptions.toSorted();
        return sorted.join('\n');
    }
}
