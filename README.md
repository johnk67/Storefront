Storefront User Manual

To start the program, run storefront.py and pass inventory.json as a postional argument (./storefront.py inventory.json).

When the program starts, it'll prompt you for your name and budget. Then, the program will take you to the menu, where you can enter a number of commands. Enter "help" to see the full list of commands available:

    list - List available parts and all their attributes in the specified category.

    details - Show details for the specified part ID.

    compatibility - Check compatibility between specified parts given their IDs.

    build - Build a custom computer with specified parts and add the computer to the shopping cart.

    remove - Remove specified part or computer from current shopping cart.

    compatibility-build - Check compatibility between all parts in current build configuration.

    budget - Set the customer's budget.

    purchase - Add the specified part to shopping cart.

    cart - View the current shopping cart.

    checkout - Complete the purchase and checkout.

    exit - Exit the program or current command.

After certain commands, the menu will prompt you for any arguments that the command requires. Part IDs may be entered in lowercase, but the following numbers must be exact (i.e. "cpu_01" = "CPU_01", "CPU_1" != "CPU_01") At any point, you can enter "exit" to return to the main menu.

When building a computer, its parts must follow the compatibility rules:
    
    Motherboard and CPU must have the same socket type.

    All instances of RAM must be the same id.

    The number of instances of RAM must be between 1 and the ram_slots on the Motherboard.

    The total power_draw of all components should be less than or equal to the power_supplied of the PSU.

After entering all the chosen parts for your custom computer, the program will automatically run compatibility_build on your computer. If the parts are not compatible, the error will be displayed, and the computer will not be added to your cart. If the parts are compatible, the computer will be added to your cart.

Whenever you are done shopping, you can enter "checkout." If you are within budget, the purchase will go through and the program will show your receipt.
