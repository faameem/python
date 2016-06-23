"""
Ask the user for a string and print out whether this string is a palindrome or not. 
(A palindrome is a string that reads the same forwards and backwards.)
"""

inputStr = input("Enter some text: ")
print(inputStr)
lstStr = list(inputStr)
print(lstStr)
revStr = list(lstStr) # if list() is not used then copy by reference
revStr.reverse()
print(revStr)
if cmp(lstStr,revStr) == 0:
    print("input string [" + inputStr + "] is a palindrome.")
else:
    print("input string [" + inputStr + "] is not a palindrome.")
    



