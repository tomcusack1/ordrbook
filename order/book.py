from bintrees import RBTree

from order.order import Order
from order.transaction import Transaction


class Book(object):
    """Each side of the Order Book has a tree instantiated.

    """
    def __init__(self):
        self.price_tree = RBTree()
        self.price_map = dict()  # Dictionary containing price : OrderList object
        self.order_map = dict()  # Dictionary containing order_id : Order object
        self.volume = 0  # Contains total quantity from all Orders in tree
        self.num_orders = 0  # Contains count of Orders in tree
        self.depth = 0  # Number of different prices in tree (http://en.wikipedia.org/wiki/Order_book_(trading)#Book_depth)

    def get_price_list(self, price):

        return self.price_map[price]

    def get_order(self, order_id):

        return self.order_map[order_id]

    def create_price(self, price):
        self.depth += 1
        new_price = Order()
        self.price_tree.insert(price, new_price)
        self.price_map[price] = new_price

    def remove_price(self, price):
        self.depth -= 1
        self.price_tree.remove(price)

        del self.price_map[price]

    def price_exists(self, price):

        return price in self.price_map

    def order_exists(self, order):

        return order in self.order_map

    def insert_order(self, quote):
        if self.order_exists(quote['order_id']):
            self.remove_order_by_id(quote['order_id'])

        self.num_orders += 1

        if quote['price'] not in self.price_map:
            self.create_price(quote['price']) # If price not in Price Map, create a node in RBtree

        order = Transaction(quote, self.price_map[quote['price']]) # Create an order
        
        self.price_map[order.price].append(order) # Add the order to the OrderList in Price Map
        self.order_map[order.order_id] = order
        self.volume += order.quantity

    def update_order(self, order_update):
        order = self.order_map[order_update['order_id']]
        original_quantity = order.quantity
        if order_update['price'] != order.price:
            # Price changed. Remove order and update tree.
            order_list = self.price_map[order.price]
            order_list.remove(order)
            if len(order_list) == 0: # If there is nothing else in the OrderList, remove the price from RBtree
                self.remove_price(order.price)
            self.insert_order(order_update)
        else:
            # Quantity changed. Price is the same.
            order.update_quantity(order_update['quantity'], order_update['timestamp'])
        self.volume += order.quantity - original_quantity

    def remove_order_by_id(self, order_id):
        self.num_orders -= 1
        order = self.order_map[order_id]
        self.volume -= order.quantity
        order.order_list.remove(order)
        if len(order.order_list) == 0:
            self.remove_price(order.price)
        del self.order_map[order_id]

    def max_price(self):
        if self.depth > 0:
            return self.price_tree.max_key()
        else:
            return None

    def min_price(self):
        if self.depth > 0:
            return self.price_tree.min_key()
        else:
            return None

    def max_price_list(self):
        if self.depth > 0:
            return self.get_price_list(self.max_price())
        else:
            return None

    def min_price_list(self):
        if self.depth > 0:
            return self.get_price_list(self.min_price())
        else:
            return None

    def __len__(self):

        return len(self.order_map)
