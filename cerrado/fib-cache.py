from functools import wraps, lru_cache


def debugger(func):
    @wraps(func)
    def decorated_func(x):
        result = func(x)
        print(f'{func.__name__}({x}) = {result}')
        return result

    return decorated_func


@debugger
@lru_cache(512)
def fib(n):
    if n == 0:
        return 0
    elif n <= 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

fib(40)