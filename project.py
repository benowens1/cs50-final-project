import sys
import csv
import re
from tabulate import tabulate


# Useages for warehouse

class Warehouse:
    def __init__(self, name):
        """
        Initalise the Warehouse with a give name.

        :param name: Name of warehouse
        :type name: str
        """
        self._name = name
        self._contents = self.load_contents()
        self._size = self.get_size()
        self._capacity = self.get_capacity()


    def __str__(self):
        """
        Return a table of contents of warehouse and the space currently take out of total capacity.
        """
        # Check for contents in the warehouse, or just presets
        if len(self._contents) > 3:
            # Print table of contents
            print(tabulate(self._contents[3:], self._contents[2]))
            print("")
            # Print storage space used thus far
            return f"Storage Space Used: {self._size}/{self._capacity}"
        else:
            return "Warehouse is empty"


    def load_contents(self):
        """
        Load the contents of the warehouse into a list.

        :return: A list of contents in warehouse
        """
        contents = []
        try:
            with open(self._name, "r") as inventory:
                reader = csv.reader(inventory)
                for row in reader:
                    contents.append(row)
        # If csv file for warehouse not found, create new one for warehouse with name "name", and return contents
        except FileNotFoundError:
            self.new_warehouse()
            with open(self._name, "r") as inventory:
                reader = csv.reader(inventory)
                for row in reader:
                    contents.append(row)
        return contents


    def new_warehouse(self):
        """
        Create a new .csv file for a new warehouse.
        """
        with open(self._name, "w", newline="") as inventory:
                # Write into the file the presets and headers
                writer = csv.writer(inventory)
                writer.writerow(["Capacity", 50])
                writer.writerow(["Total Items", 0])
                writer.writerow(["Item ID", "Item Name", "Num of Items", "Item Weight(kg)", "Item Size"])


    def get_item_data(self, item):
        """
        Get item data on the requested item from external catalog.

        :param item: Name of item to be found in catalog
        :type name: str
        :raise ValueError: If item is not in catalog
        :return: A list of data on the specific item stored in the catalog
        """
        try:
            with open("catalog.csv", "r") as catalog:
                reader = csv.reader(catalog)
                for row in reader:
                    if row[0] == item or row[1] == item:
                        return row
            raise ValueError
        except ValueError:
            return False


    def get_size(self):
        """
        Calculate the total space taken by stock in warehouse, based on item sizes and quantities.

        :return: The total space taken by items stored in warehouse
        :rtype: int
        """
        size = 0
        i = 0
        for row in self._contents:
            i += 1
            if i > 3:
                # Multiply the item size by the number in warehouse
                size += int(row[2]) * int(row[4])
        return size


    def get_capacity(self):
        """
        Get the capacity of the warehouse.

        :return: The capacity of the warehouse
        :rtype: int
        """
        capacity = int(self._contents[0][1])
        return capacity


    def add_stock(self, item, quantity):
        """
        Add stock to the warehouse.

        :param item: Item to be added to warehouse
        :type name: str
        :param quantity: Number of item
        :type quantity: int
        :raise ValueError: If not enough space in warehouse to add stock
        :return: Boolean expression for item successfully or unsuccessfully being added to warehouse
        :rtype: bool
        """
        try:
            item = str(item)
            item_data = self.get_item_data(item)
            item_id, item_name, item_weight, item_size = item_data[0], item_data[1], item_data[2], item_data[3]
            storage_space = int(item_size) * quantity

            # Check that there is enough space remaining to add new stock
            if quantity * int(item_size) > self._capacity - self._size:
                raise ValueError

            stocked = False
            for row in self._contents:
                if row[1] == item_name:
                    stocked = True
                    row[2] = str(int(row[2]) + int(quantity))
                    break
            if not stocked:
                self._contents.append([item_id, item_name, quantity, item_weight, item_size])

            # Update the space taken by stock in self._contents
            self._contents[1][1] = str(int(self._contents[1][1]) + storage_space)
            # Update the space taken by stock in self._size
            self._size += storage_space

            # Update csv file
            with open(self._name, "w", newline="") as inventory:
                writer = csv.writer(inventory)
                for row in self._contents:
                    writer.writerow(row)

            # Stock successfully added so return True
            return True

        except ValueError:
            # Stock unsuccessfully added to return False
            return False


    def remove_stock(self, item, quantity):
        """
        Remove stock from the warehouse.

        :param item: Item to be removed from warehouse
        :type name: str
        :param quantity: Number of item
        :type quantity: int
        :raise ValueError: If item not stocked, or not enough of item stocked in warehouse
        :return: Value 1-3 representing if stock removed, not enough stock to remove, or item not stocked
        :rtype: str
        """
        try:
            item = str(item)
            item_data = self.get_item_data(item)
            item_name, item_size = item_data[1], item_data[3]
            storage_space = int(item_size) * quantity
            stocked = False
            enough_stocked = False

            for row in self._contents:
                # Check if item is stocked
                if row[1] == item_name:
                    stocked = True
                    # Check for enough stock in warehouse to be removed
                    if int(row[2]) > int(quantity):
                        enough_stocked = True
                        row[2] = str(int(row[2]) - int(quantity))
                    elif int(row[2]) == int(quantity):
                        enough_stocked = True
                        self._contents.remove(row)
                    elif int(row[2]) < int(quantity):
                        enough_stocked = False
                        # Not enough of item stocked in warehouse
                        raise ValueError
                    break

            if not stocked:
                # Item not stocked in warehouse
                raise ValueError

            # Update the space taken by stock in self._contents
            self._contents[1][1] = str(int(self._contents[1][1]) - storage_space)
            # Update the space taken by stock in self._size
            self._size -= storage_space

            # Update csv file
            with open(self._name, "w", newline="") as inventory:
                writer = csv.writer(inventory)
                for row in self._contents:
                    writer.writerow(row)

            # Stock removed
            return "1"

        except ValueError:
            # Not enough of item stocked
            if stocked == True and enough_stocked == False:
                return "2"
            # Item not stocked
            elif stocked == False:
                return "3"


# User interaction code

def main():
    """
    Begin program.
    """
    input("\nPress enter to begin...")
    help_menu()
    main_menu()


def help_menu():
    """
    Print out the help menu showing the special input options.
    """
    print("\n--------------Help Menu--------------")
    print("Enter -e or --exit to close software")
    print("Enter -m or --menu to view main menu")
    print("Enter -b or --back to go back")
    print("Enter -h or --help to get help\n\n")


def special_input(i):
    """
    Check if input is one of special inputs.

    :param i: Variable input
    :type name: str
    :return: Either function, new string, or original input
    """
    if i == "-e" or i == "--exit":
        raise sys.exit("\n\nClosing software...\n")
    elif i == "-m" or i == "--menu":
        print("\n")
        return main_menu()
    elif i == "-b" or i == "--back":
        return "b"
    elif i == "-h" or i == "--help":
        return "h"
    else:
        return i


def idle(name):
    """
    Run idle state waiting for user to continue. Allow input of special case options.

    :param name: Name of warehouse
    :type name: str
    """
    while True:
        i =input("Press enter to continue...").strip().lower()

        # Check for special input
        i = special_input(i)

        # Response
        if i == "b":
            print("\n")
            return warehouse(name)
        elif i == "h":
            help_menu()
            continue
        else:
            warehouse(name)


def warehouse_exists(name):
    """
    Check that warehouse exists and return boolean result.

    :param name: Name of warehouse
    :type name: str
    :return: A boolean expression based on if the warehouse exists
    :rtype: bool
    """
    try:
        open(name, "r")
        return True
    except FileNotFoundError:
        return False


def create_new_warehouse(name):
    """
    Create new warehouse.

    :param name: Name of warehouse
    :type name: str
    :return: A string confirming the warehouse has been created
    :rtype: str
    """
    Warehouse(name)
    return "Warehouse created"


def view_catalog():
    """
    View the catalog of items that can be added or removed into the warehouse.

    :return: A string of items in catalog, in table format
    :rtype: str
    """
    catalog = []
    with open("catalog.csv", "r") as cat:
        reader = csv.reader(cat)
        for row in reader:
            catalog.append(row)
    print(tabulate(catalog[1:], catalog[0]))
    input("\nPress enter to continue...")
    print("")


def main_menu():
    """
    Show main menu and ask which management software the user wishes to access.
    """
    print("-------------Main Menu-------------")
    print("1. Catalog Management (coming soon)")
    print("2. Warehouse Inventory Management\n")
    while True:
        i = input("Choice: ").strip()

        # Check for special input
        i = special_input(i)

        # Response
        if i == "b":
            print("\n")
            return main_menu()
        elif i == "h":
            help_menu()
            continue
        elif i == "1":
            print("\n\nComing soon...\n\n")
            main_menu()
        elif i == "2":
            warehouse_name()
        else:
            print("\nInvalid input...\n")
            continue


def warehouse_name():
    """
    Ask user to input warehouse name. Allows special case inputs as-well.
    """
    while True:
        print("\n-------Warehouse Management-------")
        name = input("Warehouse Name: ").strip().lower()

        # Check for special input
        name = special_input(name)

        # Response
        if name == "b":
            print("\n")
            return main_menu()
        elif name == "h":
            help_menu()
            continue
        else:
            name = re.sub(r"\s+", "_", name) + ".csv"
            try:
                if warehouse_exists(name):
                    return warehouse(name)
                if not warehouse_exists(name):
                    raise FileNotFoundError
            except FileNotFoundError:
                print("\nWarehouse does not exist")
                while True:
                    choice = input("Would you like to create a new warehouse? (yes/no): ").strip().lower()

                    # Check for special input
                    choice = special_input(choice)

                    # Response
                    if choice == "b":
                        print("\n")
                        return warehouse_name()
                    elif choice == "h":
                        help_menu()
                        continue
                    elif choice == "yes" or choice == "y":
                        create_new_warehouse(name)
                        warehouse(name)
                    elif choice == "no" or choice == "n":
                        warehouse_name()
                    else:
                        print("\nInvalid input...\n")
                        continue


def warehouse(name):
    """
    Offer three options for how to manage warehouse.
    Based on user input, one of three functions will be ran.
    Will also accept special case inputs and return accordingly.

    :param name: Name of warehouse
    :type name: str
    :return: Function according to user prefference
    """
    print("\n1. View Warehouse")
    print("2. Add Stock")
    print("3. Remove Stock\n")
    while True:
        i = input("Choice: ").strip()

        # Check for special input
        i = special_input(i)

        # Response
        if i == "b":
            print("\n")
            return warehouse_name()
        elif i == "h":
            help_menu()
            continue
        elif i == "1":
            view_warehouse(name)
            return warehouse(name)
        elif i == "2":
            return add_stock(name)
        elif i == "3":
            return remove_stock(name)
        else:
            print("\nInvalid input...\n")
            continue


def view_warehouse(name):
    """
    Print table showing the contents of chosen warehouse.

    :param name: Name of warehouse
    :type name: str
    :return: A string of contents of warehouse, in table format
    :rtype: str
    """
    print("")
    print(Warehouse(name))
    input("\nPress enter to continue...")
    print("")


def add_stock(name):
    """
    Ask user for specific item ID or item name, accepting special case inputs.
    Ask user for number of items to add, accepting special case inputs.
    If there is enough space to add stock, add stock.
    If there is not enough space to add stock, inform user and let they try again.

    :param name: Name of warehouse
    :type name: str
    """
    warehouse_function = Warehouse(name)
    print("\n\nEnter -c or --catalog to view catalog\n")

    while True:
        item = input("Item ID or Item Name: ").strip()

        # Check for special input
        item = special_input(item)

        # Check if item is in catalog
        is_item = warehouse_function.get_item_data(item)

        # Response
        if item == "b":
            print("\n")
            return warehouse(name)
        elif item == "h":
            help_menu()
            continue
        elif item == "-c" or item == "--catalog":
            view_catalog()
            continue
        elif item == "-i" or item == "--inventory":
            view_warehouse(name)
            continue
        elif not is_item:
            print("\nError: Item not in catalog\n")
            input("Press enter to continue...")
            print("")
            continue
        else:
            while True:
                quantity = input("Amount of item: ")

                # Check special input
                quantity = special_input(quantity)

                # Response
                if quantity == "b":
                    print("\n")
                    return add_stock(name)
                elif quantity == "h":
                    help_menu()
                    continue
                elif quantity == "-c" or quantity == "--catalog":
                    view_catalog()
                    add_stock(name)
                elif item == "-i" or item == "--inventory":
                    print("")
                    view_warehouse(name)
                    remove_stock(name)
                else:
                    try:
                        quantity = int(quantity)
                        if quantity == 0:
                            print("\nError: Invalid quantity\n")
                            idle(name)
                        if warehouse_function.add_stock(item, quantity):
                            print("\nItem added\n")
                            idle(name)
                        if not warehouse_function.add_stock(item, quantity):
                            print("\nError: Not enough space in warehouse\n")
                            idle(name)

                    except ValueError:
                        print("\nInvalid input...\n")
                        continue


def remove_stock(name):
    """
    Ask user for specific item ID or item name, accepting special case inputs.
    Ask user for number of items to remove, accepting special case inputs.
    If enough of the item is stocked to remove, remove specified amount.
    If item is not stocked or not enough of item is stocked, inform user and let them try again.

    :param name: Name of warehouse
    :type name: str
    """
    warehouse_function = Warehouse(name)
    print("\n\nEnter -i or --inventory to view inventory\n")

    while True:
        item = input("Item ID or Item Name: ").strip()

        # Check for special input
        item = special_input(item)

        # Check if item is in catalog
        is_item = warehouse_function.get_item_data(item)

        # Response
        if item == "b":
            print("\n")
            return warehouse(name)
        elif item == "h":
            help_menu()
            continue
        elif item == "-i" or item == "--inventory":
            print("")
            view_warehouse(name)
            continue
        elif item == "-c" or item == "--catalog":
            print("")
            view_catalog()
            continue
        elif not is_item:
            print("\nError: Item not in catalog\n")
            input("Press enter to continue...")
            print("")
            continue
        else:
            while True:
                quantity = input("Amount of item: ")

                # Check for special input
                quantity = special_input(quantity)

                # Response
                if quantity == "b":
                    print("\n")
                    return remove_stock(name)
                elif quantity == "h":
                    help_menu()
                    continue
                elif quantity == "-i" or quantity == "--inventory":
                    print("")
                    view_warehouse(name)
                    continue
                else:
                    try:
                        quantity = int(quantity)

                        # Check for invalid quantity input
                        if quantity == 0:
                            print("\nError: Invalid amount of items\n")
                            idle(name)

                        # Try remove item from warehouse
                        result = warehouse_function.remove_stock(item, quantity)
                        if result == "1":
                            print("\nItem removed\n")
                            idle(name)
                        elif result == "2":
                            print("\nError: Not enough items stocked in warehouse\n")
                            idle(name)
                        elif result == "3":
                            print("\nError: Item not stocked in warehouse\n")
                            idle(name)

                    except ValueError:
                        print("\nInvalid input...\n")
                        continue


if __name__ == "__main__":
    main()