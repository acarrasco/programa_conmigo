// Utility functions for Sudoku

export function* chain<T>(...iterables: Iterable<T>[]): Iterable<T> {
    for (const iterable of iterables) {
        for (const value of iterable) {
            yield value;
        }
    }
}

export function* combinations<T>(elements: T[], size: number): Iterable<T[]> {
    if (size == 0 || elements.length == 0) {
        yield [];
        return;
    }

    for (let i = 0; i <= elements.length - size; i++) {
        const rest = [...elements];
        const head = elements[i];
        rest.splice(0, i + 1);
        for (const rest_combinations of combinations(rest, size - 1)) {
            yield [head, ...rest_combinations];
        }
    }
}

