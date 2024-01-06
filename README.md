   # Warehouse Management Software - Oct 2023
   ### Video Demo: <https://youtu.be/yYHsvVNXsMo>
   ### Description:
    Warehouse Management Software is a terminal-based inventory management system. It is designed to be part of a larger drone delivery management system that will take orders from stores like Amazon and deliver ordered items using a fleet of drones.

    The program allows the user to manage multiple warehouses, using the unique warehouse name. The user can create new warehouses aswell as manage existing ones. Once the warehouse is chosen/created, the user can:

    1. View Warehouse

    This will show the current contents of the warehouse in a table format, showing the unique item ID, item name, item quantity, item weight, and item size.
    It will then also show the storage space used which is (number of items * item size) / warehouse capacity. The warehouse capacity is set at a default value of 50 units.

    2. Add Stock

    Add stock gives the user the ability to add items from the defined catalog of items. The user is prompted for the item ID or item name, and then how many of this item they wish to add. Then the software will add the stock to the warehouse if, a) the item is in the catalog, and b) if there is enough storage space remaining. If either a) or b) are an issue, this is dispayed to the user, and they are prompted to either 1. View Warehouse, 2. Add Stock, or 3. Remove Stock.

    3. Remove Stock

    Remove stock gives the user the ability to remove items from the warehouse. The user is prompted for the item ID or item name, and then how many of this item they wish to remove. Then the software will remove the stock from the warehouse if, a) the item is stocked in the warehouse, and b) if there is enough of the item stocked. If either a) or b) are an issue, this is dispayed to the user, and they are prompted to either 1. View Warehouse, 2. Add Stock, or 3. Remove Stock.


    There are special command inputs which can be used by the user to navigate the software. They are as follows:

    Enter -e or --exit to close software.
    Enter -m or --menu to view main menu.
    Enter -h or --help to get help.
    Enter -b or --back to go back.
    Enter -i or --inventory to view warehouse inventory.
    Enter -c or --catalog to view catalog of items.

    These inputs can be used in all user interface instances. The software will execute the special command input based on where in the software the command is given, which is specifically relevant to the final three special commands above. For example, -i and -c will only be able to be called once inside a warehouse. If called outside of a warehouse, an error message will be displayed and another input is prompted. The output of -i and -c is the warehouse inventry and the catalog in table format respectively. Furthermore, -b will go back to the previous menu, or user prompt, when called. If -b is called in the main menu, the main menu will simply be prompted again.


   ### Program Files:
    project.py
    Contains all the files for managing warehouses. The class Warehouse represents a storage facility with the ability to load and manage its contents. It offers functionalities such as adding and removing stock items, calculating storage space, and interacting with an external catalog of items.

    catalog.csv
    CSV file containing all the items which can be added to different warehouses as stock. It holds values for Item ID, Item Name, Item Weight(kg), and Item Size. This catalog is used to determine if an item can be added to the warehouse or not. It is a representation of all the items a company sells.

    test_project.py
    Tests the warehouse management software. It tests adding and removing stock, and all their fringe cases. It also test that the storage space is correctly calculated.

    requirements.txt
    List of all libraries that the project requires.
