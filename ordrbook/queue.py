from ordrbook.order import Order
class Queue:

    def __init__(self):
        self._head: Order | None = None  # First order in the list
        self._tail: Order | None = None  # Last order in the list
        self.length: int = 0  # Number of Orders in the list
        self.volume: int = 0  # Sum of Order quantity in the list AKA share volume
        self.last: Order | None = None  # Helper for iterating

    def next_order(self):
        """Get the next order in the list.

        Set self.last as the next order. If there is no next order, stop
        iterating through list.
        """
        if self.last is None:

            raise StopIteration
        else:
            return_value = self.last
            self.last = self.last.next_order

            return return_value

    @property
    def head(self):

        return self._head

    @head.setter
    def head(self, value: Order):

        self._head = value

    @property
    def tail(self):

        return self._tail

    @tail.setter
    def tail(self, value):

        self._tail = value

    def append(self, order):
        """Appends an order to the end of the queue.
        
        Args:
            order (Order): The order to append
        """
        if self.length == 0:  # Empty queue
            order.next_order = None
            order.previous_order = None
            self.head = order
            self.tail = order
        else:  # Add to end of existing queue
            # First set the new order's links
            order.previous_order = self.tail
            order.next_order = None
            # Then update the existing tail's next_order
            self.tail.next_order = order
            # Finally update the queue's tail pointer
            self.tail = order

        self.length += 1
        self.volume += order.quantity

    def remove(self, order):
        """Removes an Order from the list.

        First grab next & previous order from the Order we are removing.
        Then relink everything. Finally, remove the Order.

        """
        self.volume -= order.quantity
        self.length -= 1

        if self.length == 0:
            self.head = None
            self._tail = None
            self.last = None
            return

        next_order = order.next_order
        previous_order = order.previous_order

        if next_order is not None and previous_order is not None:
            next_order.previous_order = previous_order
            previous_order.next_order = next_order
        elif next_order is not None:  # There is no previous order
            next_order.previous_order = None
            self.head = next_order  # The next order becomes the first order in the OrderList after this Order is removed
        elif previous_order is not None:  # There is no next order
            previous_order.next_order = None
            self.tail = previous_order  # The previous order becomes the last order in the OrderList after this Order is removed

    def move_to_tail(self, order):
        """After updating the quantity of an existing Order, move it to the tail of the OrderList

        Check to see that the quantity is larger than existing, update the quantities, then move to tail.
        """
        if order.next_order is None:
            # Order is already at tail, nothing to do
            return

        # Update links for previous order
        if order.previous_order is not None:
            order.previous_order.next_order = order.next_order
        else:
            self.head = order.next_order

        # Update links for next order
        order.next_order.previous_order = order.previous_order

        # Move order to tail
        order.previous_order = self.tail
        order.next_order = None
        self.tail.next_order = order
        self.tail = order

    def __len__(self):

        return self.length

    def __iter__(self):
        self.last = self.head

        return self
