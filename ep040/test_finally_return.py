def foo():
    try:
        return 0
    except:
        return 1
    finally:
        return 2
    
def bar():
    a = 0
    try:
        return a
    finally:
        a = 1
    

print(foo())
print(bar())