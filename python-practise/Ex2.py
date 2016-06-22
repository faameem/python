"""
Ask the user for a number. Depending on whether the number is even or odd, print out an appropriate message to the user. 
Hint: how does an even / odd number react differently when divided by 2?
"""

num = int(input("What number? "))
evenOrOdd = num % 2
if evenOrOdd == 0:
    print("even")
else:
    print("odd")
multipleOf4 = num % 4
if multipleOf4 == 0:
    print("multiple of 4")
