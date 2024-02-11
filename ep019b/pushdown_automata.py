from collections import namedtuple

Rule = namedtuple('Rule', ['character', 'top', 'push', 'pop'])
PushdownAutomaton = namedtuple('PushdownAutomaton', ['rules'])

def recognize(automaton, text):
    stack = []
    for c in text:
        t = stack[-1] if stack else None
        for rule in automaton.rules:
            if rule.character == c and (rule.top == t or not rule.top):
                if rule.pop:
                    if stack:
                        stack.pop()
                    else:
                        return False
                if rule.push:
                    stack.append(rule.push)
                break
        else:
            return False
    return not stack

balanced_parenthesis = PushdownAutomaton(
    [
        Rule('(', None, '(', False),
        Rule(')', '(', None, True),
    ]
)

# print(recognize(balanced_parenthesis, ')'))
# print(recognize(balanced_parenthesis, '('))
# print(recognize(balanced_parenthesis, '(()))'))
# print(recognize(balanced_parenthesis, '(()()'))
# print(recognize(balanced_parenthesis, ''))
# print(recognize(balanced_parenthesis, '()'))
# print(recognize(balanced_parenthesis, '(())'))
# print(recognize(balanced_parenthesis, '(()())()'))

balanced_anything = PushdownAutomaton(
    [
        Rule('(', None, '(', False),
        Rule(')', '(', None, True),
        Rule('[', None, '[', False),
        Rule(']', '[', None, True),
        Rule('{', None, '{', False),
        Rule('}', '{', None, True),
    ]
)

print(recognize(balanced_anything, '(}'))
print(recognize(balanced_anything, '({)}'))
print(recognize(balanced_anything, ''))
print(recognize(balanced_anything, '({})'))
print(recognize(balanced_anything, '([]{})'))
print(recognize(balanced_anything, '[()()]({[[]{}]})'))
