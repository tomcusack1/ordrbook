from math import log10

from blkchn import Blockchain
from ordrbook.book import Book


class OrderBook:
    """Creates an order book.

    Attributes:
      blockchain (Blockchain): All trades stored on a blockchain
      bids (Book): The bid side of the order book
      asks (Book): The ask side of the order book

    """
    def __init__(self, tick_size=0.0001):
        """Constructor for Order Book.

        Args:
          tick_size (float): Rounds all prices up to this tick size

        """
        self.blockchain = Blockchain()
        self.bids = Book()
        self.asks = Book()
        self.tick_size = tick_size

    def order(self, quote: dict):
        """Places an order onto the order book and attempts to find a matching `ask` or `bid` order."""
        trades = list()
        quantity = quote['quantity']
        price = round(quote['price'], int(log10(1 / self.tick_size)))

        if quote['type'] == 'bid':
            while self.asks and price > self.asks.min_price() and quantity > 0:
                best_price_asks = self.asks.min_price_list()
                quantity, new_trades = self.process_orders(side='ask',
                                                           orders=best_price_asks,
                                                           quantity=quantity,
                                                           quote=quote)
                trades += new_trades

            if quantity > 0:
                quote['quantity'] = quantity
                self.bids.insert_order(quote)

        elif quote['type'] == 'ask':
            while self.bids and price < self.bids.max_price() and quantity > 0:
                best_price_bids = self.bids.max_price_list()
                quantity, new_trades = self.process_orders(side='bid',
                                                           orders=best_price_bids,
                                                           quantity=quantity,
                                                           quote=quote)
                trades += new_trades

            if quantity > 0:
                quote['quantity'] = quantity
                self.asks.insert_order(quote)

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

            # Add new trade as a transaction on the ledger
            self.blockchain.new_transaction(sender=head_order.order_id,
                                            recipient=quote['trade_id'],
                                            amount=str(traded_price),
                                            quantity=str(traded_quantity))

            # Immediately create a new block. In the future, we should (1) broadcast to all connected nodes that we
            # have a new trade and (2) create a new block every N trades, rather than on each trade.
            last_block = self.blockchain.last_block
            proof = self.blockchain.proof_of_work(last_block)
            previous_hash = self.blockchain.hash(last_block)
            self.blockchain.new_block(proof, previous_hash)

        return quantity, trades
