from decimal import Decimal

import pytest

from ordrbook.orderbook import OrderBook
from ordrbook.book import Book


@pytest.fixture
def empty_orderbook():
    return OrderBook()


@pytest.fixture
def orderbook_with_orders():
    ob = OrderBook()
    bid = {
        "order_id": "bid1",
        "quantity": 5,
        "price": Decimal("100.50"), 
        "timestamp": 1234567890,
        "trade_id": "trade1"
    }
    ask = {
        "order_id": "ask1",
        "quantity": 3,
        "price": Decimal("101.50"),
        "timestamp": 1234567890, 
        "trade_id": "trade2"
    }
    ob.process_order(bid, "bid")
    ob.process_order(ask, "ask")
    return ob


def test_orderbook_initialization(empty_orderbook):
    assert isinstance(empty_orderbook.bids, Book)
    assert isinstance(empty_orderbook.asks, Book)
    assert empty_orderbook.bids.depth == 0
    assert empty_orderbook.asks.depth == 0


def test_cancel_bid_order(orderbook_with_orders):
    orderbook_with_orders.cancel_order("bid1", "bid")
    
    assert orderbook_with_orders.bids.depth == 0
    assert "bid1" not in orderbook_with_orders.bids.orders
    assert orderbook_with_orders.asks.depth == 1


def test_cancel_ask_order(orderbook_with_orders):
    orderbook_with_orders.cancel_order("ask1", "ask")
    
    assert orderbook_with_orders.asks.depth == 0
    assert "ask1" not in orderbook_with_orders.asks.orders
    assert orderbook_with_orders.bids.depth == 1


def test_modify_bid_order(orderbook_with_orders):
    update = {
        "order_id": "bid1",
        "quantity": 7,
        "price": Decimal("100.50"),
        "timestamp": 1234567890
    }
    orderbook_with_orders.modify_order(update, "bid")
    
    assert orderbook_with_orders.bids.orders["bid1"].quantity == Decimal("7")
    assert orderbook_with_orders.bids.volume == Decimal("7")


def test_modify_ask_order(orderbook_with_orders):
    update = {
        "order_id": "ask1",
        "quantity": 4,
        "price": Decimal("102.50"),
        "timestamp": 1234567890
    }
    orderbook_with_orders.modify_order(update, "ask")
    
    assert orderbook_with_orders.asks.orders["ask1"].quantity == Decimal("4")
    assert orderbook_with_orders.asks.orders["ask1"].price == Decimal("102.50")


def test_best_bid_ask(orderbook_with_orders):
    assert orderbook_with_orders.best_bid() == Decimal("100.50")
    assert orderbook_with_orders.best_ask() == Decimal("101.50")


def test_empty_best_bid_ask(empty_orderbook):
    assert empty_orderbook.best_bid() is None
    assert empty_orderbook.best_ask() is None
