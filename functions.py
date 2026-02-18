#!/usr/bin/env python3
"""
Defines functions for storefront.py.
"""

import json
from typing import List

import objects

# User-defined Exception for invalid parts.
class PartException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# Takes json file as input and creates an object for each component.
# Returns a dictionary that maps the part ID to the part's object.
def create_inventory(json_file):
    try:
        with open(json_file, encoding = "utf-8") as file:
            dic = json.load(file)["inventory"]
    except TypeError as exc:
        print(f"Problem - {exc}")
        print(f'{type(exc) = }')

    inventory = {}
    for entry in dic:
        item = entry["item"]
        if "CPU" == item["type"]:
            inventory[item["id"]] = objects.CPU(item["id"],
                                                item["type"],
                                                item["name"],
                                                item["price"],
                                                item["power_draw"],
                                                item["socket"])
        elif "GPU" == item["type"]:
            inventory[item["id"]] = objects.GPU(item["id"],
                                                item["type"],
                                                item["name"],
                                                item["price"],
                                                item["power_draw"],
                                                item["overclockable"])
        elif "RAM" == item["type"]:
            inventory[item["id"]] = objects.RAM(item["id"],
                                                item["type"],
                                                item["name"],
                                                item["price"],
                                                item["power_draw"],
                                                item["capacity"])
        elif "PSU" == item["type"]:
            inventory[item["id"]] = objects.PSU(item["id"],
                                                item["type"],
                                                item["name"],
                                                item["price"],
                                                item["power_supplied"])
        elif "Motherboard" == item["type"]:
            inventory[item["id"]] = objects.Motherboard(item["id"],
                                                item["type"],
                                                item["name"],
                                                item["price"],
                                                item["power_draw"],
                                                item["socket"],
                                                item["ram_slots"])

        elif "Storage" == item["type"]:
            inventory[item["id"]] = objects.Storage(item["id"],
                                                item["type"],
                                                item["name"],
                                                item["price"],
                                                item["capacity"])
    return inventory

#List all available commands and their function.
def list_commands():
    commands = {"list": ("List available parts and all their attributes in the "
                         "specified category."),
                "details": "Show details for the specified part ID.",
                "compatibility": ("Check compatibility between specified parts "
                                  "given their IDs."),
                "build": ("Build a custom computer with specified parts and "
                          "add the computer to the shopping cart."),
                "remove": ("Remove specified part or computer from current "
                           "shopping cart."),
                "compatibility-build": ("Check compatibility between all parts "
                                        "in current build configuration."),
                "budget": "Set the customer's budget.",
                "purchase": "Add the specified part to shopping cart.",
                "cart": "View the current shopping cart.",
                "checkout": "Complete the purchase and checkout.",
                "exit": "Exit the program or current command.\n"}
    print("All available commands:")
    for key, value in commands.items():
        print(f"\t{key} - {value}")

# List available parts and all their attributes in the specified category.
def list_parts(inventory, category = ""):
    if category == "":
        for item in inventory.values():
            print(f"{item.details()}")
    elif category in ["CPU", "GPU", "RAM", "PSU", "Motherboard", "Storage"]:
        for item in inventory.values():
            if category == item.type:
                print(f"{item.details()}")


# Show details for the specified part ID.
def details(inventory, part_id):
    if isinstance(part_id, objects.Computer):
        print(f"{part_id.details()}")
    elif part_id in inventory:
        print(f"{inventory[part_id].details()}")
    else:
        raise PartException("Part not found.\n")

# Check compatibility between specified parts given their IDs.
def compatibility(inventory, part_id1, part_id2):
    # Initialize variables.
    compatible = True
    if part_id1 not in inventory:
        raise PartException("Part 1 ID is invalid.\n")
    if part_id2 not in inventory:
        raise PartException("Part 2 ID is invalid.\n")
    part1 = inventory[part_id1]
    part2 = inventory[part_id2]

    # Verify that the parts follow compatibility rules.
    if (part1.type == "Motherboard" and part2.type == "CPU" or
            part1.type == "CPU" and part2.type == "Motherboard"):
        compatible = part1.socket == part2.socket
        if not compatible:
            print("Motherboard and CPU must have the same socket type.\n")
    elif part1.type == "RAM" and part2.type == "RAM":
        compatible = part1.id == part2.id
        if not compatible:
            print("All instances of RAM must be the same id.\n")

    if compatible:
        print("Parts are compatible.\n")
    return compatible

# Build a custom computer with specified parts and add the computer to
# the shopping cart.
def build(customer: objects.Customer, cid, motherboard: objects.Motherboard,
          rams: List[objects.RAM], cpu: objects.CPU, psu: objects.PSU,
          storage: objects.Storage, storage2: objects.Storage = None,
          gpu: objects.GPU = None):
    computer = objects.Computer(cid, motherboard, rams, cpu, psu, storage,
                                storage2, gpu)
    compatibility_build(computer)
    customer.cart.append(computer)
    customer.total += computer.price
    return computer

# Remove specified part(s) or computer(s) from current shopping cart.
def remove(customer: objects.Customer, inventory, item, *items):
    if isinstance(item, objects.Computer):
        customer.cart.remove(item)
        customer.total -= item.price
        print(f"{item} removed from cart.\n")
    elif item in inventory:
        if inventory[item] in customer.cart:
            customer.cart.remove(inventory[item])
            customer.total -= inventory[item].price
            print(f"{item} removed from cart.\n")
        else:
            raise PartException(f"{item} not in cart.\n")
    else:
        raise PartException(f"{item} is not a valid part ID.\n")

    for extra in items:
        if isinstance(extra, objects.Computer):
            customer.cart.remove(extra)
            customer.total -= extra.price
            print(f"{extra} removed from cart.\n")
        elif extra in inventory:
            if inventory[extra] in customer.cart:
                customer.cart.remove(inventory[extra])
                customer.total -= inventory[extra].price
                print(f"{extra} removed from cart.\n")
            else:
                raise PartException(f"{extra} not in cart.\n")
        else:
            raise PartException(f"{extra} is not a valid part ID.\n")

# Check compatibility between all parts in current build configuration.
def compatibility_build(computer):
    # Initialize variables.
    ram_ids = set()

    for ram in computer.rams:
        ram_ids.add(ram)

    # Check motherboard and CPU socket types.
    if computer.motherboard.socket != computer.cpu.socket:
        raise PartException(("Motherboard and CPU must have the same socket "
                            "type."))

    # Check RAM IDs.
    if 1 < len(ram_ids):
        raise PartException("All instances of RAM must be the same id.")

    # Check number of RAMs.
    if (0 == len(computer.rams) or
            len(computer.rams) > computer.motherboard.ram_slots):
        raise PartException(f"The number of RAMs ({len(computer.rams)}) cannot "
               "exceed the number of RAM slots "
               f"({computer.motherboard.ram_slots}).")

    # Check power draw.
    if computer.power_draw > computer.psu.power_supplied:
        raise PartException("The total power draw from all components, "
               f"{computer.power_draw}W, should be less than "
               "or equal to the power supplied by the PSU, "
               f"{computer.psu.power_supplied}W.")

    print((f"The parts in the current build configuration of {computer} "
              "are compatible.\n"))
    return True

# Add the specified part to shopping cart.
def purchase(customer: objects.Customer, inventory, part_id):
    if part_id not in inventory:
        raise PartException("Part not found.\n")
    customer.cart.append(inventory[part_id])
    customer.total += inventory[part_id].price
    print(f"{part_id} added to cart.\n")

# Complete the purchase and checkout.
def checkout(customer: objects.Customer):
    if not customer.cart:
        print("Cannot checkout, your cart is empty.\n")
    elif customer.budget < customer.total:
        print("Cannot checkout, items in cart are over the budget.\n")
    else:
        customer.budget -= customer.total
        print("Order submitted. Your order is on the way.")
        for item in customer.cart:
            print(f"\t{item}")
        print(f"Your total is ${customer.total}.00.\n")
        customer.cart.clear()
        customer.total = 0
