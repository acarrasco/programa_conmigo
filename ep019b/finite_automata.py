from collections import namedtuple

Rule = namedtuple('Rule', ['character', 'next_state'])
State = namedtuple('State', ['name', 'is_accepted', 'rules'])
FiniteStateAutomaton = namedtuple('FiniteStateAutomaton', ['start', 'states'])

def recognize(automaton, text):
    state = next(s for s in automaton.states if s.name == automaton.start)
    for c in text:
        for rule in state.rules:
            if rule.character == c:
                state = next(s for s in automaton.states if s.name == rule.next_state)
                break
        else:
            return False
    return state.is_accepted

decimal_numbers = FiniteStateAutomaton(
    'integer',
    [
        State('integer', True, [
            Rule(str(d), 'integer') for d in range(10)
        ] + [
            Rule('.', 'decimal_transition')
        ]),
        State('decimal_transition', False, [
            Rule(str(d), 'decimal') for d in range(10)
        ]),
        State('decimal', True, [
            Rule(str(d), 'decimal') for d in range(10)
        ])
    ]
)

print(recognize(decimal_numbers, "abcd"))
print(recognize(decimal_numbers, "123.12451.1"))
print(recognize(decimal_numbers, "123."))
print(recognize(decimal_numbers, "123"))
print(recognize(decimal_numbers, "123.1325"))
