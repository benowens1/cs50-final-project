import pytest
import os
from project import Warehouse


TEST_WAREHOUSE_CSV = "test_warehouse.csv"


@pytest.fixture(autouse=True)
def setup_teardown():
    if os.path.exists(TEST_WAREHOUSE_CSV):
        os.remove(TEST_WAREHOUSE_CSV)

    yield

    if os.path.exists(TEST_WAREHOUSE_CSV):
        os.remove(TEST_WAREHOUSE_CSV)


def test_add_stock():
    warehouse = Warehouse(TEST_WAREHOUSE_CSV)

    assert warehouse.add_stock("AirPods", 5) == True
    assert warehouse.add_stock("AeroPress", 5) == True


def test_no_capacity_add():
    warehouse = Warehouse(TEST_WAREHOUSE_CSV)

    assert warehouse.add_stock("AirPods", 25)
    assert warehouse.add_stock("AirPods", 24)
    assert warehouse.add_stock("AeroPress", 1) == False
    assert warehouse.add_stock("Notebook", 1) == False
    assert warehouse.add_stock("AirPods", 1)


def test_add_item_not_in_catalog():
    warehouse = Warehouse(TEST_WAREHOUSE_CSV)

    with pytest.raises(SystemExit) as exc_info:
        warehouse.add_stock("Football", 1)
    assert str(exc_info.value) == "Item not in catalog"


def test_removing_stock():
    warehouse = Warehouse(TEST_WAREHOUSE_CSV)
    warehouse.add_stock("AirPods", 5)
    warehouse.add_stock("AeroPress", 5)

    assert warehouse.remove_stock("AirPods", 5) == "1"
    assert warehouse.remove_stock("AeroPress", 1) == "1"


def test_remove_not_stocked():
    warehouse = Warehouse(TEST_WAREHOUSE_CSV)
    warehouse.add_stock("AirPods", 5)

    assert warehouse.remove_stock("AirPods", 10) == "2"
    assert warehouse.remove_stock("AeroPress", 5) == "3"


def test_remove_not_in_catalog():
    warehouse = Warehouse(TEST_WAREHOUSE_CSV)

    with pytest.raises(SystemExit) as exc_info:
        warehouse.remove_stock("Football", 1)
    assert str(exc_info.value) == "Item not in catalog"


def test_total_items_count():
    warehouse = Warehouse(TEST_WAREHOUSE_CSV)
    warehouse.add_stock("AirPods", 5)
    warehouse.add_stock("AeroPress", 3)

    assert int(warehouse._contents[1][1]) == 11


def test_remaining_space():
    warehouse = Warehouse(TEST_WAREHOUSE_CSV)
    warehouse.add_stock("AirPods", 5)
    warehouse.add_stock("AeroPress", 3)

    capacity = int(warehouse._contents[0][1])
    used_space = warehouse.get_size()
    remaining_space = capacity - used_space

    assert remaining_space == 39