from collections import deque
from math import log10
from time import time

from ordrbook.book import Book


class OrderBook:
    """Creates an order book.

    Attributes:
      tape (deque): A list of all the trades. 0th position is the most recent trade
      bids (Book): The bid side of the order book
      asks (Book): The ask side of the order book

    """
    def __init__(self, tick_size=0.0001):
        """Constructor for Order Book.

        Args:
          tick_size (float): Rounds all prices up to this tick size

        """
        self.tape = deque(maxlen=None)
        self.bids = Book()
        self.asks = Book()
        self.tick_size = tick_size

    def bid(self, quote: dict):
        """Places an `bid` order onto the order book and attempts to find a matching `ask` order."""
        order_in_book = None
        trades = list()
        quantity = quote['quantity']
        price = round(quote['price'], int(log10(1 / self.tick_size)))

        while self.asks and price > self.asks.min_price() and quantity > 0:
            best_price_asks = self.asks.min_price_list()
            quantity, new_trades = self.process_orders(side='ask', orders=best_price_asks, quantity=quantity, quote=quote)
            trades += new_trades

        if quantity > 0:
            quote['quantity'] = quantity
            self.bids.insert_order(quote)
            order_in_book = quote

        return trades, order_in_book

    def ask(self, quote):
        """Places an `ask` order onto the order book and attempts to find a matching `bid` order."""
        order_in_book = None
        trades = list()
        quantity = quote['quantity']
        price = round(quote['price'], int(log10(1 / self.tick_size)))

        while self.bids and price < self.bids.max_price() and quantity > 0:
            best_price_bids = self.bids.max_price_list()
            quantity, new_trades = self.process_orders(side='bid', orders=best_price_bids, quantity=quantity, quote=quote)
            trades += new_trades

        if quantity > 0:
            quote['quantity'] = quantity
            self.asks.insert_order(quote)
            order_in_book = quote

        return trades, order_in_book

    def process_orders(self, side: str, orders, quantity, quote):
        """Takes a group of orders at the same price and matches them with an appropriate order given the quantity."""
        trades = list()

        while len(orders) > 0 and quantity > 0:

            head_order = orders.head
            traded_price = head_order.price

            if quantity < head_order.quantity:
                traded_quantity = quantity
                new_book_quantity = head_order.quantity - quantity
                head_order.update_quantity(new_book_quantity, head_order.timestamp)
                quantity = 0

            elif quantity == head_order.quantity:
                traded_quantity = quantity
                if side == 'bid':
                    self.bids.remove_order_by_id(head_order.order_id)
                else:
                    self.asks.remove_order_by_id(head_order.order_id)
                    quantity = 0
            else:
                # Quantity to trade is larger than the head order
                traded_quantity = head_order.quantity
                if side == 'bid':
                    self.bids.remove_order_by_id(head_order.order_id)
                else:
                    self.asks.remove_order_by_id(head_order.order_id)
                    quantity -= traded_quantity

            transaction = {
                'created_at': int(time()),
                'price': traded_price,
                'quantity': traded_quantity,
                'buyer': head_order.order_id,
                'seller': quote['trade_id']
            }

            self.tape.append(transaction)
            trades.append(transaction)

        return quantity, trades
