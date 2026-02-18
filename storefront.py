#!/usr/bin/env python3
"""
A program that allows users to purchase individual computer components from
an inventory, or build a complete custom computer.
"""
import sys

import objects
import functions

def main():
    # Ensure inventory.json is passed as a positional argument when running
    # this program.
    if len(sys.argv) != 2:
        raise IndexError("Pass inventory.json as positional argument.")

    # Load inventory.json into a Python dictionary that maps part IDs to their
    # respective object.
    inventory = functions.create_inventory(sys.argv[1])

    # Prompt user for their name and budget.
    name = input("Enter your name: ")
    while True:
        try:
            budget_amt = float(input("Enter your budget: "))
        except ValueError:
            print("Please enter a numerical amount.")
        else:
            break

    # Create new customer with given name and budget.
    customer = objects.Customer(name, budget_amt)
    computer = None

    command = input((f"Hello {customer.name}, how can I help you today? "
                     "Enter \'help\' to see all commands: "))

    while "exit" != command:
        if "help" == command:
            functions.list_commands()

        elif "list" == command:
            # Prompt user for a specific category to list.
            while True:
                category = input(("Enter a category (Motherboard, "
                                  "RAM, CPU, PSU, Storage, GPU) "
                                  "or press enter to see all "
                                  "available parts.\n"))
                if "exit" == category:
                    break
                elif category in ["", "CPU", "GPU", "RAM", "PSU",
                                  "Motherboard", "Storage"]:
                    functions.list_parts(inventory, category)
                    break
                print("Not a valid category.")

        elif "details" == command:
            # Prompt user for a specific part ID.
            while True:
                part_id = input("Enter a part ID: ").upper()
                if "EXIT" == part_id:
                    break
                try:
                    if part_id == computer.id:
                        functions.details(inventory, computer)
                    else:
                        functions.details(inventory, part_id)
                except functions.PartException as exc:
                    print(f"Error: {exc.value}")
                else:
                    break

        elif "compatibility" == command:
            # Prompt user for 2 part IDs.
            while True:
                part_id1 = input("Enter a part ID: ").upper()
                if "EXIT" == part_id1:
                    break
                part_id2 = input("Enter a second part ID: ").upper()
                if "EXIT" == part_id2:
                    break
                try:
                    functions.compatibility(inventory, part_id1, part_id2)
                except functions.PartException as exc:
                    print(f"Error: {exc.value}")
                else:
                    break

        elif "build" == command:
            # Prompt user for computer components.
            computer_id = input("Enter a computer ID: ").upper()
            while True:
                motherboard = input("Enter a motherboard ID: ").upper()
                if "EXIT" == motherboard:
                    break
                elif motherboard in ["MB_01", "MB_02", "MB_03",
                                     "MB_04", "MB_05"]:
                    motherboard = inventory[motherboard]
                    break
                print("Not a valid motherboard ID.")
            while True:
                ram_objects_list = []
                rams = input("Enter ram IDs separated by a space: ").upper()
                if "EXIT" == rams:
                    break
                rams_list = rams.split()
                valid_rams = True
                # Check if RAM IDs are valid.
                for ram in rams_list:
                    if ram not in ["RAM_01", "RAM_02", "RAM_03",
                                   "RAM_04", "RAM_05"]:
                        valid_rams = False
                    else:
                        ram_objects_list.append(inventory[ram])
                if valid_rams:
                    break
                print("Invalid RAM ID(s).")
            while True:
                cpu = input("Enter a CPU ID: ").upper()
                if "EXIT" == cpu:
                    break
                elif cpu in ["CPU_01", "CPU_02", "CPU_03",
                             "CPU_04", "CPU_05"]:
                    cpu = inventory[cpu]
                    break
                print("Not a valid CPU ID.")
            while True:
                psu = input("Enter a PSU ID: ").upper()
                if "EXIT" == psu:
                    break
                elif psu in ["PSU_01", "PSU_02", "PSU_03",
                             "PSU_04", "PSU_05"]:
                    psu = inventory[psu]
                    break
                print("Not a valid PSU ID.")
            while True:
                storage = input("Enter a storage ID: ").upper()
                if "EXIT" == storage:
                    break
                elif storage in ["STORAGE_01", "STORAGE_02", "STORAGE_03",
                                 "STORAGE_04", "STORAGE_05"]:
                    storage = inventory[storage]
                    break
                print("Not a valid storage ID.")
            while True:
                storage2 = input(("Enter another storage ID or "
                                  "press enter to skip: ")).upper()
                if "EXIT" == storage2:
                    break
                elif storage2 in ["STORAGE_01", "STORAGE_02", "STORAGE_03",
                                  "STORAGE_04", "STORAGE_05"]:
                    storage2 = inventory[storage2]
                    break
                elif "" == storage2:
                    storage2 = None
                    break
                print("Not a valid storage ID.")
            while True:
                gpu = input("Enter a GPU ID or press enter to skip: ").upper()
                if "EXIT" == gpu:
                    break
                elif gpu in ["GPU_01", "GPU_02", "GPU_03", "GPU_04", "GPU_05"]:
                    gpu = inventory[gpu]
                    break
                elif "" == gpu:
                    gpu = None
                    break
                print("Not a valid GPU ID.")
            try:
                computer = functions.build(customer, computer_id, motherboard,
                                 ram_objects_list, cpu, psu, storage,
                                 storage2, gpu)
            except AttributeError:
                print("Could not build computer.\n")
            except functions.PartException as err:
                print(f"Could not build computer: {err}\n")

        elif "remove" == command:
            # Prompt user for specific part/computer ID(s).
            while True:
                part_ids = input(("Enter part/computer ID(s) "
                                  "separated by a space: ")).upper()
                if "EXIT" == part_ids:
                    break
                part_ids_list = part_ids.split()
                # Check if ID is a computer.
                for item in part_ids_list:
                    if computer:
                        if item == computer.id:
                            part_ids_list.remove(item)
                            part_ids_list.append(computer)
                try:
                    functions.remove(customer, inventory, *part_ids_list)
                except functions.PartException as exc:
                    print(f"Error: {exc.value}")
                else:
                    break
                if not customer.cart:
                    print("Cart is empty.\n")
                    break

        elif "compatibility-build" == command:
            if not computer:
                print("Build a computer first.\n")
            else:
                functions.compatibility_build(computer)

        elif "budget" == command:
            # Prompt user for new budget.
            while True:
                try:
                    new_budget = float(input("Enter your budget: "))
                except ValueError:
                    print("Please enter a numerical amount.")
                else:
                    break
            customer.budget = new_budget
            print(f"Your new budget is ${customer.budget:.2f}\n")

        elif "purchase" == command:
            # Prompt user for a part ID.
            while True:
                part_id = input("Enter a part ID: ").upper()
                if "EXIT" == part_id:
                    break
                try:
                    functions.purchase(customer, inventory, part_id)
                except functions.PartException as exc:
                    print(f"Error: {exc.value}")
                else:
                    break

        elif "cart" == command:
            customer.view_cart()

        elif "checkout" == command:
            functions.checkout(customer)

        command = input("Enter a command: ")

if __name__ == "__main__":
    main()
