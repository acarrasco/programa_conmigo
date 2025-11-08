type FilledBoard = { [index: number]: number };
type PossibleValues = { [coordinate_index: number]: Set<number> };

import { chain, combinations } from './utils';

export class SudokuBoard {
    private possible_values: PossibleValues;
    private size: number;

    constructor(
        private region_rows: number,
        private region_columns: number,
        private initial_values: FilledBoard,
    ) {
        this.size = region_rows * region_columns;
        this.possible_values = this.initialize_possible_values();
    }

    coordinate2index(i: number, j: number) {
        return i * this.size + j;
    }

    get_possible_values(i: number, j: number) {
        return this.possible_values[this.coordinate2index(i, j)];
    }

    *row_neighbor_indices(i: number, j: number) {
        for (let nj = 0; nj < this.size; nj++) {
            if (nj === j) continue;
            yield this.coordinate2index(i, nj);
        }
    }

    *column_neighbor_indices(i: number, j: number) {
        for (let ni = 0; ni < this.size; ni++) {
            if (ni === i) continue;
            yield this.coordinate2index(ni, j);
        }
    }

    *region_neighbor_indices(i: number, j: number) {
        let region_i = Math.floor(i / this.region_rows);
        let region_j = Math.floor(j / this.region_columns);

        for (let ni = region_i * this.region_rows; ni < (region_i + 1) * this.region_rows; ni++) {
            for (let nj = region_j * this.region_columns; nj < (region_j + 1) * this.region_columns; nj++) {
                if (ni === i && nj === j) continue;
                yield this.coordinate2index(ni, nj);
            }
        }
    }

    initialize_possible_values(): PossibleValues {
        const all_possible_values: number[] = [];
        for (let n = 1; n <= this.size; n++) {
            all_possible_values.push(n);
        }

        const possible_values: PossibleValues = {};

        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                const idx = this.coordinate2index(i, j);
                if (this.initial_values[idx]) {
                    possible_values[idx] = new Set([this.initial_values[idx]]);
                }
                else {
                    possible_values[idx] = new Set(all_possible_values);
                }
            }
        }

        return possible_values;
    }

    print_possible_values() {
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                const idx = this.coordinate2index(i, j);
                const values = Array.from(this.possible_values[idx]).join(', ');
                console.log(`(${i}, ${j}) = {${values}}`);
            }
        }
    }

    *common_sets(neighbor_idxs: number[], set_size: number): Iterable<Set<number>> {
        const indices_with_possible_values_of_set_size = neighbor_idxs.filter(idx => this.possible_values[idx].size <= set_size);

        for (const indices_combination of combinations(indices_with_possible_values_of_set_size, set_size)) {
            const possible_values_array = indices_combination.map(idx => this.possible_values[idx]);
            const possible_values_union = new Set<number>();
            for (const pv_set of possible_values_array) {
                for (const val of pv_set) {
                    possible_values_union.add(val);
                }
            }
            if (possible_values_union.size == set_size) {
                yield possible_values_union;
            }
        }
    }

    reduce_possibilities(i: number, j: number): boolean {
        const possible_values = this.get_possible_values(i, j);

        if (possible_values.size == 1) {
            return false;
        }

        const initial_possible_values_size = possible_values.size;
        for (let set_size = 1; set_size < this.size - 1; set_size++) {

            for (const covered_set of chain(
                this.common_sets([...this.row_neighbor_indices(i, j)], set_size),
                this.common_sets([...this.column_neighbor_indices(i, j)], set_size),
                this.common_sets([...this.region_neighbor_indices(i, j)], set_size)
            )) {
                for (const covered_value of covered_set) {
                    possible_values.delete(covered_value);
                }
            }
            if (possible_values.size != initial_possible_values_size) {
                return true;
            }
        }
        return false;
    }

    solve() {
        let keep_going = true;
        while (keep_going) {
            keep_going = false;
            for (let i = 0; i < this.size; i++) {
                for (let j = 0; j < this.size; j++) {
                    if (this.reduce_possibilities(i, j)) {
                        keep_going = true;
                    }
                }
            }
        }
    }

    pretty_print_possible_values() {
        // Find max width for each cell
        let cell_width = 0;
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                const idx = this.coordinate2index(i, j);
                const values = Array.from(this.possible_values[idx]).join(',');
                cell_width = Math.max(cell_width, values.length);
            }
        }
        cell_width = Math.max(cell_width, 3);

        // Helper to draw horizontal region boundary
        function draw_horizontal_boundary(region_columns: number, size: number, cell_width: number) {
            let line = "";
            for (let j = 0; j < size; j++) {
                if (j % region_columns === 0) line += "+";
                line += "-".repeat(cell_width + 2);
            }
            line += "+";
            return line;
        }

        for (let i = 0; i < this.size; i++) {
            // Print horizontal region boundary
            if (i % this.region_rows === 0) {
                console.log(draw_horizontal_boundary(this.region_columns, this.size, cell_width));
            }
            let row = "";
            for (let j = 0; j < this.size; j++) {
                if (j % this.region_columns === 0) {
                    row += "|";
                }
                const idx = this.coordinate2index(i, j);
                const values = Array.from(this.possible_values[idx]).join(',');
                row += " " + values.padEnd(cell_width, ' ') + " ";
            }
            row += "|";
            console.log(row);
        }
        // Print bottom boundary
        console.log(draw_horizontal_boundary(this.region_columns, this.size, cell_width));
    }
}

// Main function to parse command line arguments and read from stdin
function main() {
    // Parse command line arguments
    const args = process.argv.slice(2);

    if (args.length !== 3) {
        console.error('Usage: node sudoku.js <region_rows> <region_columns> <input_file>');
        process.exit(1);
    }

    const region_rows = parseInt(args[0]);
    const region_columns = parseInt(args[1]);
    const input_file = args[2];

    if (isNaN(region_rows) || isNaN(region_columns) || region_rows <= 0 || region_columns <= 0) {
        console.error('Error: region_rows and region_columns must be positive integers');
        process.exit(1);
    }

    const fs = require('fs');
    let input = '';
    try {
        input = fs.readFileSync(input_file, 'utf8');
    } catch (err) {
        console.error(`Error reading file: ${input_file}`);
        process.exit(1);
    }

    // Parse initial values from input
    const numbers = input.trim().split(/\s+/).map(num => parseInt(num));

    // Convert to FilledBoard format (index -> value mapping)
    const initial_values: FilledBoard = {};
    const board_size = region_rows * region_columns;

    if (numbers.length !== board_size * board_size) {
        console.error(`Error: Expected ${board_size * board_size} numbers, got ${numbers.length}`);
        process.exit(1);
    }

    for (let i = 0; i < numbers.length; i++) {
        if (numbers[i] !== 0) {  // 0 represents empty cell
            initial_values[i] = numbers[i];
        }
    }

    console.log('Initial board values:');
    for (let i = 0; i < board_size; i++) {
        let row = '';
        for (let j = 0; j < board_size; j++) {
            const idx = i * board_size + j;
            row += (initial_values[idx] || 0) + ' ';
        }
        console.log(row.trim());
    }

    // Create and solve the Sudoku board
    const board = new SudokuBoard(region_rows, region_columns, initial_values);
    console.log('Initial possible values:');
    board.print_possible_values();
    board.solve();
    console.log('Possible values after solving:');
    board.pretty_print_possible_values();
}

// Run main function if this script is executed directly
if (require.main === module) {
    main();
}

