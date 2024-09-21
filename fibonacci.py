def fibonacci(n):
  if n <= 0:
    return 0
  elif n == 1:
    return 1
  else:
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage:
n = 10
result = fibonacci(n)
print("The", n, "th Fibonacci number is:", result)
----------
x = 10

if x > 15:
  print("x is greater than 15")
elif x > 5:
  print("x is greater than 5 but less than or equal to 15")
else:
  print("x is less than or equal to 5")
