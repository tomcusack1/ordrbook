import pytest
from decimal import Decimal

from ordrbook.queue import Queue
from ordrbook.order import Order


@pytest.fixture
def empty_queue():
    return Queue()


@pytest.fixture
def queue_with_order():
    queue = Queue()
    order = Order({
        "order_id": "test1",
        "quantity": 5,
        "price": Decimal("100.50"), 
        "timestamp": 1234567890,
        "trade_id": "trade1"
    }, queue)
    queue.append(order)
    return queue


def test_empty_queue_initialization(empty_queue):
    assert empty_queue.head is None
    assert empty_queue.tail is None
    assert empty_queue.length == 0
    assert empty_queue.volume == 0
    assert empty_queue.last is None


def test_append_order(empty_queue):
    order = Order({
        "order_id": "test1",
        "quantity": 5,
        "price": Decimal("100.50"),
        "timestamp": 1234567890,
        "trade_id": "trade1"
    }, empty_queue)
    
    empty_queue.append(order)
    
    assert empty_queue.head == order
    assert empty_queue.tail == order
    assert empty_queue.length == 1
    assert empty_queue.volume == Decimal("5")
    assert order.next_order is None
    assert order.previous_order is None


def test_append_multiple_orders(empty_queue):
    order1 = Order({
        "order_id": "test1",
        "quantity": 5,
        "price": Decimal("100.50"),
        "timestamp": 1234567890,
        "trade_id": "trade1"
    }, empty_queue)
    
    order2 = Order({
        "order_id": "test2", 
        "quantity": 3,
        "price": Decimal("100.50"),
        "timestamp": 1234567890,
        "trade_id": "trade2"
    }, empty_queue)
    
    empty_queue.append(order1)
    empty_queue.append(order2)
    
    assert empty_queue.head == order1
    assert empty_queue.tail == order2
    assert empty_queue.length == 2
    assert empty_queue.volume == Decimal("8")
    assert order1.next_order == order2
    assert order2.previous_order == order1


def test_remove_order(queue_with_order):
    order = queue_with_order.head
    queue_with_order.remove(order)
    
    assert queue_with_order.head is None
    assert queue_with_order.tail is None
    assert queue_with_order.length == 0
    assert queue_with_order.volume == 0


def test_remove_middle_order(empty_queue):
    order1 = Order({
        "order_id": "test1",
        "quantity": 5,
        "price": Decimal("100.50"),
        "timestamp": 1234567890,
        "trade_id": "trade1"
    }, empty_queue)
    
    order2 = Order({
        "order_id": "test2",
        "quantity": 3,
        "price": Decimal("100.50"),
        "timestamp": 1234567890,
        "trade_id": "trade2"
    }, empty_queue)
    
    order3 = Order({
        "order_id": "test3",
        "quantity": 4,
        "price": Decimal("100.50"),
        "timestamp": 1234567890,
        "trade_id": "trade3"
    }, empty_queue)
    
    empty_queue.append(order1)
    empty_queue.append(order2)
    empty_queue.append(order3)
    
    empty_queue.remove(order2)
    
    assert empty_queue.length == 2
    assert empty_queue.volume == Decimal("9")
    assert order1.next_order == order3
    assert order3.previous_order == order1


def test_next_order_iteration(empty_queue):
    order1 = Order({
        "order_id": "test1",
        "quantity": 5,
        "price": Decimal("100.50"),
        "timestamp": 1234567890,
        "trade_id": "trade1"
    }, empty_queue)
    
    order2 = Order({
        "order_id": "test2",
        "quantity": 3,
        "price": Decimal("100.50"),
        "timestamp": 1234567890,
        "trade_id": "trade2"
    }, empty_queue)
    
    empty_queue.append(order1)
    empty_queue.append(order2)
    
    empty_queue.last = empty_queue.head
    
    assert empty_queue.next_order() == order1
    assert empty_queue.next_order() == order2
    
    with pytest.raises(StopIteration):
        empty_queue.next_order()
