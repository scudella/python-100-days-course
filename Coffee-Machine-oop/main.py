from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()
is_on = True

while is_on:
    order_name = input(f"What would you like? ({menu.get_items()}) " )
    if order_name == "off":
        break
    elif order_name == "report":
        coffee_maker.report()
        money_machine.report()

    else:
        menu_item = menu.find_drink(order_name)
        if menu_item is None:
            print("")
        else:
            if coffee_maker.is_resource_sufficient(menu_item):
                if money_machine.make_payment(menu_item.cost):
                    coffee_maker.make_coffee(menu_item)
                else:
                    print("Sorry, that's not enough money. Money refunded.")
