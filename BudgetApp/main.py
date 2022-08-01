import budget
from budget import MoneySpentGraphic
from unittest import main

food = budget.Category("Food")
food.DepositMoney(1000, "initial deposit")
food.WithDrawMoney(10.15, "groceries")
food.WithDrawMoney(15.89, "restaurant and more food for dessert")
print(food.MoneyBalance())

clothing = budget.Category("Clothing")
food.TransferMoney(50, clothing)
clothing.WithDrawMoney(25.55)
clothing.WithDrawMoney(100)

auto = budget.Category("Auto")
auto.DepositMoney(1000, "initial deposit")
auto.WithDrawMoney(15)

print(food)
print(clothing)

print(MoneySpentGraphic([food, clothing, auto]))

# Run unit tests automatically
main(module='tests', exit=False)