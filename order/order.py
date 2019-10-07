from decimal import * 


class Order:
    """Orders represent the core piece of the exchange. Every bid/ask is an Order.
    Orders are doubly linked and have helper functions (next_order, prev_order)
    to help the exchange fulfill orders with quantities larger than a single
    existing Order.

    """
    def __init__(self, quote, order_list):
        self.timestamp = int(quote['timestamp'])  # Integer Unix timestamp
        self.quantity = Decimal(quote['quantity'])  # Quantity can be partial amounts
        self.price = Decimal(quote['price'])
        self.order_id = quote['order_id']
        self.trade_id = int(quote['trade_id'])
        self.next_order = None
        self.previous_order = None
        self.order_list = order_list

    def next_order(self):

        return self.next_order

    def previous_order(self):

        return self.previous_order

    def update_quantity(self, new_quantity, new_timestamp):
        if new_quantity > self.quantity and self.order_list.tail != self:
            # check to see that the order is not the last order in list and the quantity is more
            self.order_list.move_to_tail(self) # move to the end
        self.order_list.volume -= (self.quantity - new_quantity) # update volume
        self.timestamp = new_timestamp
        self.quantity = new_quantity
