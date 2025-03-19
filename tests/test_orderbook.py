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
        "trade_id": "trade1",
        "type": "bid"
    }
    ob.order(bid)
    
    return ob


def test_match_orders(orderbook_with_orders):
    ask = {
        "order_id": "ask1",
        "quantity": 3,
        "price": Decimal("101.50"),
        "timestamp": 1234567890, 
        "trade_id": "trade2",
        "type": "ask"
    }
    # We have 1 bid on the order book. If we add an ask at 101.50, it should match
    # and the quantity of the bid should be reduced by 3.
    assert orderbook_with_orders.bids.depth == 1
    orderbook_with_orders.order(quote=ask)
    assert orderbook_with_orders.asks.depth == 1
    assert orderbook_with_orders.bids.volume == 5
    assert orderbook_with_orders.asks.volume == 3
    

def test_orderbook_initialization(empty_orderbook):
    assert isinstance(empty_orderbook.bids, Book)
    assert isinstance(empty_orderbook.asks, Book)
    assert empty_orderbook.bids.depth == 0
    assert empty_orderbook.asks.depth == 0
