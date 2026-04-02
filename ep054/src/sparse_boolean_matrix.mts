
export class SparseBooleanMatrix<R extends string, C extends string> {

    private rows: Partial<Record<R, Set<C>>> = {};
    private cols: Partial<Record<C, Set<R>>> = {};

    constructor(row_headers: R[], col_headers: C[]) {
        for (const r of row_headers) {
            this.rows[r] = new Set<C>();
        }
        for (const c of col_headers) {
            this.cols[c] = new Set<R>();
        }
    }

    public deleteRow(r: R): Set<C> {
        const row = this.rows[r];
        if (!row) {
            throw new Error(`Missing row ${r}`);
        }
        for (const c of row) {
            const col = this.cols[c];
            if (!col) {
                throw new Error(`Missing col ${c}`);
            }
            col.delete(r);
        }
        delete this.rows[r];
        return row;
    }

    public deleteColumn(c: C): Set<R> {
        const col = this.cols[c];
        if (!col) {
            throw new Error(`Missing col ${c}`);
        }
        for (const r of col) {
            const row = this.rows[r];
            if (!row) {
               throw new Error(`Missing row ${r}`);
            }
            row.delete(c);
        }
        delete this.cols[c];
        return col;
    }

    public addRow(r: R, row: Set<C>) {
        this.rows[r] = row;
        for (const c of row) {
            const col = this.cols[c];
            if (!col) {
                throw new Error(`Missing col ${c}`);
            }
            col.add(r);
        }
    }

    public addColumn(c: C, col: Set<R>) {
        this.cols[c] = col;
        for (const r of col) {
            const row = this.rows[r];
            if (!row) {
               throw new Error(`Missing row ${r}`);
            }
            row.add(c);
        }
    }

    public setElement(r: R, c: C) {
        const row = this.rows[r];
        if (!row) {
            throw new Error(`Missing row ${r}`);
        }        
        row.add(c);

        const col = this.cols[c];
        if (!col) {
            throw new Error(`Missing col ${c}`);
        }
        col.add(r);
    }

    public hasRow(r: R): boolean {
        return Object.hasOwn(this.rows, r);
    }

    public hasColumn(c: C): boolean {
        return Object.hasOwn(this.cols, c);
    }

    public getRows(): Partial<Record<R, Set<C>>> {
        return this.rows;
    }

    public getColumns(): Partial<Record<C, Set<R>>> {
        return this.cols;
    }
}
