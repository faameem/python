"""
Create a program that asks the user to enter their name and their age. 
Print out a message addressed to them that tells them the year that they will turn 100 years old.
"""
age = int(input("What is your age: "))
year100 = 2016 + 100 - age
print("You turn 100 in " + str(year100))
num = int(input("How many messages? "))
print(num * ("You turn 100 in " + str(year100) + ". "))
print(num * ("You turn 100 in " + str(year100) + "\n"))