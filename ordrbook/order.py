from decimal import Decimal


class Order:
    """Orders represent the core piece of the exchange. Every bid/ask is an Order.
    Orders are doubly linked and have helper functions (next_order, prev_order)
    to help the exchange fulfill orders with quantities larger than a single
    existing Order.

    Args:
        quote (dict): A dictionary containing the order details.
            Required keys:
                - 'timestamp': int
                - 'quantity': int
                - 'price': Decimal
                - 'order_id': str
                - 'trade_id': str

    """
    def __init__(self, quote: dict, order_list):
        self.timestamp: int = int(quote["timestamp"])  # Integer Unix timestamp
        self.quantity: int = int(quote["quantity"])  # Quantity can be partial amounts
        self.price: Decimal = Decimal(quote["price"])
        self.order_id: str = quote["order_id"]
        self.trade_id: str = quote["trade_id"]
        self.next_order: Order | None = None
        self.previous_order: Order | None = None
        self.order_list = order_list

    def next_order(self):
        """Returns the next order in the order list."""

        return self.next_order

    def previous_order(self):
        """Returns the previous order in the order list."""
        return self.previous_order

    def update_quantity(self, new_quantity: int, new_timestamp: int):
        """Updates the quantity of shares outstanding to be bought/sold."""
        if new_quantity > self.quantity and self.order_list.tail != self:
            # Check to see that the order is not the last order in list and the quantity is more
            self.order_list.move_to_tail(self)  # Move to the end

        self.order_list.volume -= self.quantity - new_quantity
        self.timestamp = new_timestamp
        self.quantity = new_quantity
