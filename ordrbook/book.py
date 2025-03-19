from decimal import Decimal

from bintrees import RBTree

from ordrbook.queue import Queue
from ordrbook.order import Order


class Book:
    def __init__(self):
        self.tree = RBTree()
        self.prices: dict[Decimal, Queue] = dict()  # { price : Queue } objects
        self.orders: dict[str, Order] = dict()  # { order_id : Order } objects
        self.volume: int = 0  # Contains total quantity from all Orders in tree
        self.num_orders: int = 0  # Contains count of orders in tree
        self.depth: int = 0  # Number of different prices in tree

    def get_price_list(self, price: float) -> dict:

        return self.prices[price]

    def get_order(self, order_id):

        return self.orders[order_id]

    def create_price(self, price):
        self.depth += 1
        new_price = Queue()
        self.tree.insert(price, new_price)
        self.prices[price] = new_price

    def remove_price(self, price: Decimal):
        """Removes a price from the book.
        
        Args:
            price (Decimal): The price to remove.

        """
        self.depth -= 1
        self.tree.remove(price)

        del self.prices[price]

    def price_exists(self, price):

        return price in self.prices

    def order_exists(self, order):

        return order in self.orders

    def insert_order(self, quote: dict):
        """Adds an order to the book.
        
        Args:
            quote (dict): A dictionary containing the order details.
                Required keys:
                    - 'order_id': str
                    - 'quantity': int
                    - 'price': Decimal
                    - 'timestamp': str
                    - 'trade_id': str

        """
        if self.order_exists(quote["order_id"]):
            self.remove_order_by_id(quote["order_id"])

        self.num_orders += 1

        if quote["price"] not in self.prices:
            # If price not in price list, create a node in tree
            self.create_price(quote["price"])

        order = Order(quote, self.prices[quote["price"]])  # Create an order

        self.prices[order.price].append(order)  # Add the order to the prices queue
        self.orders[order.order_id] = order
        self.volume += order.quantity

    def update_order(self, order_update: dict):
        """Updates an order in the book.
        
        Args:
            order_update (dict): A dictionary containing the updated order details.
                Required keys:
                    - 'order_id': str
                    - 'quantity': int
                    - 'price': Decimal
                    - 'timestamp': str
                    - 'trade_id': str

        """
        order = self.orders[order_update["order_id"]]
        original_quantity = order.quantity
        
        if order_update["price"] != order.price:
            # Price changed. Remove order and update tree.
            order_list = self.prices[order.price]
            order_list.remove(order)
            if len(order_list) == 0:
                # If there is nothing else in the OrderList, remove the price from RBtree
                self.remove_price(order.price)
            
            # Remove the order from orders dict before inserting updated version
            del self.orders[order_update["order_id"]]
            self.num_orders += 1  # Compensate for the removal
            
            self.insert_order(order_update)
        else:
            # Quantity changed. Price is the same.
            order.update_quantity(int(order_update["quantity"]), int(order_update["timestamp"]))
            self.volume += int(order_update["quantity"]) - original_quantity

    def remove_order_by_id(self, order_id: str):
        """Removes an order from the book by order_id.
        
        Args:
            order_id (str): The ID of the order to remove.

        """
        self.num_orders -= 1
        order = self.orders[order_id]
        self.volume -= order.quantity
        order.order_list.remove(order)

        if order.order_list.length <= 0:
            self.remove_price(order.price)

        del self.orders[order_id]

    def max_price(self):
        if self.depth > 0:
            return self.tree.max_key()
        else:
            return None

    def min_price(self):
        if self.depth > 0:
            return self.tree.min_key()
        else:
            return None

    def max_price_list(self):
        if self.depth > 0:
            return self.get_price_list(price=self.max_price())
        else:
            return None

    def min_price_list(self):
        if self.depth > 0:
            return self.get_price_list(price=self.min_price())
        else:
            return None

    def __len__(self):

        return len(self.orders)
