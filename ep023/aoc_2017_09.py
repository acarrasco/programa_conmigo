from collections import namedtuple

Rule = namedtuple('Rule', ['character', 'top', 'push', 'pop', 'callback'])
PushdownAutomaton = namedtuple('PushdownAutomaton', ['rules'])

def recognize(automaton, text):
    stack = []
    for c in text:
        t = stack[-1] if stack else None
        for rule in automaton.rules:
            if (not rule.character or rule.character == c) and (not rule.top or rule.top == t):
                if rule.pop:
                    if stack:
                        stack.pop()
                    else:
                        return False
                if rule.push:
                    stack.append(rule.push)
                if rule.callback:
                    rule.callback(c, stack)
                break
        else:
            return False
    return not stack


def make_automaton(group_callback, garbage_callback):
    return PushdownAutomaton([
        Rule(character=None, top='!', push=None, pop=True, callback=None),
        Rule(character='!', top=None, push='!', pop=False, callback=None),
        Rule(character='>', top='<', push=None, pop=True, callback=None),
        Rule(character=None, top='<', push=None, pop=False, callback=garbage_callback),
        Rule(character='<', top=None, push='<', pop=False, callback=None),
        Rule(character='{', top=None, push='{', pop=False, callback=group_callback),
        Rule(character='}', top='{', push=None, pop=True, callback=None),
        Rule(character=None, top=None, push=None, pop=False, callback=None),
    ])

def calculate_score(text):
    '''
    >>> calculate_score('{}')
    (1, 0)
    >>> calculate_score('{{{}}}')
    (6, 0)
    >>> calculate_score('{{},{}}')
    (5, 0)
    >>> calculate_score('{{{},{},{{}}}}')
    (16, 0)
    >>> calculate_score('{<a>,<a>,<a>,<a>}')
    (1, 4)
    >>> calculate_score('{{<ab>},{<ab>},{<ab>},{<ab>}}')
    (9, 8)
    >>> calculate_score('{{<!!>},{<!!>},{<!!>},{<!!>}}')
    (9, 0)
    >>> calculate_score('{{<a!>},{<a!>},{<a!>},{<ab>}}')
    (3, 17)
    '''
    score = 0
    garbage = 0
    def group_callback(c, stack):
        nonlocal score
        score += len(stack)
    def garbage_callback(c, stack):
        nonlocal garbage
        garbage += 1

    automaton = make_automaton(group_callback, garbage_callback)
    _success = recognize(automaton, text)
    return score, garbage

if __name__ == '__main__':
    input = open('input.txt').readline()
    score, garbage = calculate_score(input.strip())
    print(score)
    print(garbage)
