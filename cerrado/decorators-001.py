def debugger(func):
  def decorated_func(x):
     result = func(x)
     print(f'{func.__name__}({x}) = {result}')
     return result
      
  return decorated_func
      
 
@debugger
def fib(n):
  if n <= 1:
    return 1
  else:
    return fib(n - 1) + fib(n - 2)