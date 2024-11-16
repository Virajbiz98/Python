import math

def cal():
    c = input("Enter an operator (+ - * / ^ √ %): ")
    a = float(input("Enter the 1st number: "))
    b = float(input("Enter the 2nd number: "))
    

    match c: # check the value of c 
        case "+":
            print(a + b)
        case "-":
            print(a - b)
        case "*":
            print(a * b)
        case "/":
            print(a / b)
        case "^":
            print(a ** b)
        case "√":
            print( math.sqrt(a))
        case "%":
            print(a  * (b / 100))
        case _:
            print("It's not a valid operator")

cal() # call the function 
 





