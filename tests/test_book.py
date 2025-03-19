from decimal import Decimal

import pytest

from ordrbook.book import Book


@pytest.fixture
def empty_book():
    return Book()


@pytest.fixture
def book_with_order():
    book = Book()
    order = {
        "order_id": "test1",
        "quantity": 5,
        "price": Decimal("100.50"),
        "timestamp": "1234567890",
        "trade_id": "trade1"
    }
    book.insert_order(order)
    return book


def test_empty_book_initialization(empty_book):
    assert empty_book.tree is not None
    assert len(empty_book.prices) == 0
    assert len(empty_book.orders) == 0
    assert empty_book.volume == 0
    assert empty_book.num_orders == 0
    assert empty_book.depth == 0


def test_insert_order(empty_book):
    order = {
        "order_id": "test1", 
        "quantity": 5,
        "price": Decimal("100.50"),
        "timestamp": "1234567890",
        "trade_id": "trade1"
    }
    empty_book.insert_order(quote=order)
    assert empty_book.depth == 1
    assert empty_book.num_orders == 1
    assert empty_book.volume == 5
    assert "test1" in empty_book.orders
    assert Decimal("100.50") in empty_book.prices


def test_remove_order(book_with_order):
    book_with_order.remove_order_by_id("test1")
    assert book_with_order.depth == 0
    assert book_with_order.num_orders == 0
    assert book_with_order.volume == 0
    assert len(book_with_order.orders) == 0
    assert len(book_with_order.prices) == 0


def test_update_order_quantity(book_with_order):
    update = {
        "order_id": "test1",
        "quantity": 5,
        "price": Decimal("100.50"),
        "timestamp": "1234567890"
    }
    book_with_order.update_order(update)
    
    assert book_with_order.volume == 5
    assert book_with_order.orders["test1"].quantity == 5


def test_update_order_price(book_with_order):
    update = {
        "order_id": "test1",
        "quantity": 5,
        "price": Decimal("101.50"),
        "timestamp": "1234567890"
    }
    book_with_order.update_order(update)
    
    assert Decimal("101.50") in book_with_order.prices
    assert Decimal("100.50") not in book_with_order.prices
    assert book_with_order.orders["test1"].price == Decimal("101.50")


def test_max_min_price(book_with_order):
    assert book_with_order.max_price() == Decimal("100.50")
    assert book_with_order.min_price() == Decimal("100.50")
    
    # Add another order at different price
    order2 = {
        "order_id": "test2",
        "quantity": 5,
        "price": Decimal("99.50"),
        "timestamp": "1234567890",
        "trade_id": "trade2"
    }
    book_with_order.insert_order(order2)
    
    assert book_with_order.max_price() == Decimal("100.50")
    assert book_with_order.min_price() == Decimal("99.50")


def test_empty_book_max_min_price(empty_book):
    assert empty_book.max_price() is None
    assert empty_book.min_price() is None
