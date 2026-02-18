#!/usr/bin/env python3
"""
Defines objects for storefront.py.
"""

from typing import List


class Customer:
    """Class representing a customer."""
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget
        self.cart = []
        self.total = 0

    # Set the customer's budget.
    def set_budget(self, amount):
        self.budget = amount

    # View the current shopping cart.
    def view_cart(self):
        print("Shopping Cart:")
        for item in self.cart:
            print(f"\t{item}")
        print(f"Total: ${self.total}.00")
        print(f"Your budget: ${self.budget:.2f}\n")

class Component:
    """Class representing a computer component."""
    def __init__(self, component_id, component_type, name, price):
        self.id = component_id
        self.type = component_type
        self.name = name
        self.price = price

    def details(self):
        return (f"ID: {self.id}\n"
                f"\tType: {self.type}\n"
                f"\tName: {self.name}\n"
                f"\tPrice: ${self.price}.00\n")

    def __str__(self):
        return f"{self.id}"

class CPU(Component):
    def __init__(self, cpu_id, cpu_type, name, price, power_draw, socket):
        super().__init__(cpu_id, cpu_type, name, price)
        self.power_draw = power_draw
        self.socket = socket

    def details(self):
        return super().details() + (f"\tPower Draw: {self.power_draw}W\n"
                                    f"\tSocket: {self.socket}\n")

class GPU(Component):
    def __init__(self, gpu_id, gpu_type, name, price, power_draw,
                 overclockable):
        super().__init__(gpu_id, gpu_type, name, price)
        self.power_draw = power_draw
        self.overclockable = overclockable

    def details(self):
        return super().details() + (f"\tPower Draw: {self.power_draw}W\n"
                                    f"\tOverclockable: {self.overclockable}\n")

class RAM(Component):
    def __init__(self, ram_id, ram_type, name, price, power_draw, capacity):
        super().__init__(ram_id, ram_type, name, price)
        self.power_draw = power_draw
        self.capacity = capacity

    def details(self):
        return super().details() + (f"\tPower Draw: {self.power_draw}W\n"
                                    f"\tCapacity: {self.capacity}GB\n")

class PSU(Component):
    def __init__(self, psu_id, psu_type, name, price, power_supplied):
        super().__init__(psu_id, psu_type, name, price)
        self.power_supplied = power_supplied

    def details(self):
        return super().details() + f"\tPower Supplied: {self.power_supplied}W\n"

class Motherboard(Component):
    def __init__(self, mb_id, mb_type, name, price, power_draw, socket,
                 ram_slots):
        super().__init__(mb_id, mb_type, name, price)
        self.power_draw = power_draw
        self.socket = socket
        self.ram_slots = ram_slots

    def details(self):
        return super().details() + (f"\tPower Draw: {self.power_draw}W\n"
                                    f"\tSocket: {self.socket}\n"
                                    f"\tRam Slots: {self.ram_slots}\n")

class Storage(Component):
    def __init__(self, storage_id, storage_type, name, price, capacity):
        super().__init__(storage_id, storage_type, name, price)
        self.capacity = capacity

    def details(self):
        return super().details() + f"\tCapacity: {self.capacity}GB\n"

class Computer():
    """Class representing a computer."""
    def __init__(self, cid, motherboard: Motherboard, rams: List[RAM],
                 cpu: CPU, psu: PSU, storage: Storage, storage2: Storage = None,
                 gpu: GPU = None):
        self.id = cid
        self.motherboard = motherboard
        self.rams = rams
        self.cpu = cpu
        self.psu = psu
        self.storage = storage
        self.storage2 = storage2
        self.gpu = gpu

        # Calculate total power draw and total price.
        self.power_draw = self.motherboard.power_draw + self.cpu.power_draw
        self.price = self.motherboard.price + self.cpu.price + self.psu.price \
                     + self.storage.price
        for ram in self.rams:
            self.power_draw += ram.power_draw
            self.price += ram.price
        if self.storage2:
            self.price += self.storage2.price
        if self.gpu:
            self.power_draw += self.gpu.power_draw
            self.price += self.gpu.price

    def details(self):
        dets = (f"ID: {self.id}\n"
               f"\tMotherboard: {self.motherboard.id}\n"
               f"\tRAMs: {", ".join(ram.id for ram in self.rams)}\n"
               f"\tCPU: {self.cpu.id}\n"
               f"\tPSU: {self.psu.id}\n"
               f"\tHard Drive: {self.storage.id}\n")
        if self.storage2:
            dets += f"\tHard Drive 2: {self.storage2.id}\n"
        if self.gpu:
            dets += f"\tGPU: {self.gpu.id}\n"
        return dets

    def __str__(self):
        return f"{self.id}"
