from collections import deque
from math import log10
from time import time

from order.book import Book


class OrderBook(object):
    """Creates an order book

    Example:

        quote = {
            'order_id': str(uuid4()),
            'trade_id': str(uuid4()),
            'timestamp': 1521462189,
            'type': 'bid',
            'quantity': 10,
            'price': 100.,
            'type': 'limit'
        }

    """
    def __init__(self, tick_size=0.0001):
        self.tape = deque(maxlen=None)  # 0th position is the most recent trade
        self.bids = Book()
        self.asks = Book()
        self.last_tick = None
        self.last_timestamp = 0
        self.tick_size = tick_size
        self.time = 0
        self.next_order_id = 0

    def bid_market_order(self, quote):
        trades = list()
        quantity = quote['quantity']

        while quantity > 0 and self.asks:
            best_price_asks = self.asks.min_price_list()
            quantity, new_trades = self.process_orders('ask', best_price_asks, quantity, quote)
            trades += new_trades

        return trades

    def ask_market_order(self, quote):
        trades = list()
        quantity = quote['quantity']

        while quantity > 0 and self.bids:
            best_price_bids = self.bids.max_price_list()
            quantity, new_trades = self.process_orders('bid', best_price_bids, quantity, quote)
            trades += new_trades

        return trades

    def bid_limit_order(self, quote):
        order_in_book = None
        trades = list()
        quantity = quote['quantity']
        price = round(quote['price'], int(log10(1 / self.tick_size)))

        while self.asks and price > self.asks.min_price() and quantity > 0:
            best_price_asks = self.asks.min_price_list()
            quantity, new_trades = self.process_orders(side='ask', orders=best_price_asks,
                                                       quantity=quantity, quote=quote)
            trades += new_trades

        if quantity > 0:
            quote['quantity'] = quantity
            self.bids.insert_order(quote)
            order_in_book = quote

        return trades, order_in_book

    def ask_limit_order(self, quote):
        order_in_book = None
        trades = list()
        quantity = quote['quantity']
        price = round(quote['price'], int(log10(1 / self.tick_size)))

        while self.bids and price < self.bids.max_price() and quantity > 0:
            best_price_bids = self.bids.max_price_list()
            quantity, new_trades = self.process_orders(side='bid', orders=best_price_bids,
                                                       quantity=quantity, quote=quote)
            trades += new_trades

        if quantity > 0:
            quote['quantity'] = quantity
            self.asks.insert_order(quote)
            order_in_book = quote

        return trades, order_in_book

    def process_orders(self, side, orders, quantity, quote):
        """Takes a group of orders at the same price and matches them with an appropriate order given the quantity.

        """
        trades = list()

        while len(orders) > 0 and quantity > 0:

            head_order = orders.head
            traded_price = head_order.price
            counter_party = head_order.trade_id

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

            transaction_record = {
                'timestamp': int(time()),
                'price': traded_price,
                'quantity': traded_quantity,
                'time': int(time())
            }

            if side == 'bid':
                transaction_record['party1'] = [counter_party, 'bid', head_order.order_id]
                transaction_record['party2'] = [quote['trade_id'], 'ask', None]
            else:
                transaction_record['party1'] = [counter_party, 'ask', head_order.order_id]
                transaction_record['party2'] = [quote['trade_id'], 'bid', None]

            self.tape.append(transaction_record)
            trades.append(transaction_record)

        return quantity, trades
