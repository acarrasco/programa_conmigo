import z from 'zod';

const Coordinates = z.tuple([z.int().min(0), z.int().min(0)])
const Direction = z.enum(['R', 'D', 'L', 'U']);

const SameValue = z.literal('=');
const DifferentValue = z.literal('x');
const Restriction = z.union([SameValue, DifferentValue])

const RestrictionDef = z.tuple([Coordinates, Direction, Restriction]);

const Sun = z.literal('s');
const Moon = z.literal('m');
const Value = z.union([Sun, Moon]);

const ValueDef = z.tuple([Coordinates, Value]);

export const Input = z.object({
    "rows": z.int().default(6),
    "cols": z.int().default(6),
    "restrictions": z.array(RestrictionDef),
    "values": z.array(ValueDef),
});

export type Input = z.infer<typeof Input>;
export type Value = z.infer<typeof Value>;
export type ValueDef = z.infer<typeof ValueDef>;
export type Coordinates = z.infer<typeof Coordinates>;
export type Direction = z.infer<typeof Direction>;
export type RestrictionDef = z.infer<typeof RestrictionDef>;