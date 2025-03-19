from decimal import Decimal

import pytest

from ordrbook.order import Order
from ordrbook.queue import Queue


@pytest.fixture
def empty_queue():
    return Queue()


def test_order_initialization(empty_queue):
    order_data = {
        "order_id": "test1",
        "quantity": 5,
        "price": Decimal("100.50"), 
        "timestamp": 1234567890,
        "trade_id": "trade1"
    }
    order = Order(order_data, empty_queue)

    assert order.order_id == "test1"
    assert order.quantity == 5
    assert order.price == Decimal("100.50")
    assert order.timestamp == 1234567890
    assert order.trade_id == "trade1"
    assert order.next_order is None
    assert order.previous_order is None
    assert order.order_list == empty_queue


def test_update_quantity():
    queue = Queue()
    order = Order(quote={
        "order_id": "test1",
        "quantity": 5,
        "price": Decimal("100.50"),
        "timestamp": 1234567890,
        "trade_id": "trade1"
    }, order_list=queue)

    order.update_quantity(new_quantity=10, new_timestamp=1234567891)

    assert order.quantity == 10
    assert order.timestamp == 1234567891


def test_order_linking():
    queue = Queue()
    order1 = Order({
        "order_id": "test1",
        "quantity": 5,
        "price": Decimal("100.50"),
        "timestamp": "1234567890",
        "trade_id": "trade1"
    }, queue)

    order2 = Order({
        "order_id": "test2",
        "quantity": 3,
        "price": Decimal("100.50"), 
        "timestamp": "1234567890",
        "trade_id": "trade2"
    }, queue)

    queue.append(order1)
    queue.append(order2)

    assert order1.next_order == order2
    assert order2.previous_order == order1
    assert order1.previous_order is None
    assert order2.next_order is None
