import { expect } from 'chai';
import { chain, combinations } from '../src/utils';


describe('combinations', () => {
    it('should generate zero length combinations', () => {
        const result = Array.from(combinations([1, 2, 3], 0));
        expect(result).to.deep.equal([[]]);
    });

    it('should generate combinations of size 1', () => {
        const result = Array.from(combinations([1, 2, 3], 1));
        expect(result).to.deep.equal([[1], [2], [3]]);
    });

    it('should generate combinations of size 2', () => {
        const result = Array.from(combinations([1, 2, 3], 2));
        expect(result).to.deep.equal([[1, 2], [1, 3], [2, 3]]);
    });

    it('should generate combinations of size 3', () => {
        const result = Array.from(combinations([1, 2, 3], 3));
        expect(result).to.deep.equal([[1, 2, 3]]);
    });

});

describe('chain', () => {
    it('should chain multiple iterables', () => {
        const result = Array.from(chain([1, 2], [3, 4], [5, 6]));
        expect(result).to.deep.equal([1, 2, 3, 4, 5, 6]);
    });
    
    it('should handle empty iterables', () => {
        const result = Array.from(chain([], [1, 2], []));
        expect(result).to.deep.equal([1, 2]);
    });

});