from tkinter import Menu

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

def report(resources, money):
    print(f"Water: {resources['water']}ml\n"
          f"Milk: {resources['milk']}ml\n"
          f"Coffee: {resources['coffee']}g\n"
          f"Money: ${money:.2f}")

def prompt_for_money(cost):
     print("Please insert coins.")
     quarters = int(input("How many quarters?: "))
     dimes = int(input("How many dimes?: "))
     nickles = int(input("How many nickles?: "))
     pennies = int(input("How many pennies?: "))
     money_received = quarters * 0.25 + dimes * 0.10 + nickles * 0.05 + pennies * 0.01
     return round(money_received - cost, 2)

def make_the_drink(ingredients, resources, choice):
    result = check_for_ingredients(ingredients, resources)
    has_missing_ingredient = not all(result.values())
    if has_missing_ingredient:
        missing_ingredient = " "
        for item in result:
            if not result[item]:
                missing_ingredient += item + ", "
        print(f"Sorry, there is not enough {missing_ingredient}")
        return False
    else:
        update_resources(ingredients, resources)
        print(f"Here is your {choice}. Enjoy!")
        return True


def check_for_ingredients(ingredients, resources):
    missing_ingredient = {
        "water": True,
        "milk": True,
        "coffee": True,
    }
    for ingredient in ingredients:
        if ingredients[ingredient] > resources[ingredient]:
            missing_ingredient[ingredient] = False
    return missing_ingredient

def update_resources(ingredients, resources):
    for ingredient in ingredients:
        resources[ingredient] -= ingredients[ingredient]

money = 0.0
while True:
    choice = input("What would you like? (espresso/latte/cappuccino): ")
    if choice == "off":
        break
    if choice == "report":
        report(resources, money)
    if choice == "espresso" or choice == "latte" or choice == "cappuccino":
        change = prompt_for_money(MENU[choice]["cost"])
        if change < 0:
            print(f"Sorry, you need extra {change * -1}. Here is your money back!")
            break
        else:
            print(f"Here is {change} in change.")
            if(make_the_drink(MENU[choice]["ingredients"], resources, choice)):
                money += MENU[choice]["cost"]
