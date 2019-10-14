# A Python Implementation of a Limit Order Book

A limit orders describes:

  1. If it is a buy (bid) or a sell (ask) order
  2. The maximum quantity to trade
  3. The limit price. For a buyer this is the maximum they will pay for a share (or contract). For a seller, it is the opposite - It is the least they are willing to accept.

A trade needs both a buyer and a seller. The exchanges role is to get the buyers and seller the best possibile price, through a process is called 'matching'. The matching rules determines which orders get filled and which stay within the Limit Order Book (LOB).

The algorithm used in this application is called the Price Time algorithm. This is the most common algorithm used in exchanges today, but there are other rules worth of note - The Price ProRata and the Price TimeProRata rules.

Not everything trades this way. Some brokers fill orders within their own brokerages, where a buyer and seller are clients with the broker, thus an exchange is not needed. Also, some brokers pay to use Dark Pools, but these topics are out of the scope of this introduction.

Consider the following orders:

| Buy Orders    	| Sell Orders   	|
|---------------	|---------------	|
| B1 : 10 @ 99  	| S1 : 30 @ 99  	|
| B2 : 40 @ 99  	| S2 : 20 @ 101 	|
| B3 : 20 @ 100 	| S3 : 10 @ 100 	|

They arrive in the following order:

![Trade Order](https://latex.codecogs.com/png.latex?\large&space;b_{1}&space;\rightarrow&space;b_{2}&space;\rightarrow&space;s_{1}&space;\rightarrow&space;b_{3}&space;\rightarrow&space;s_{2}&space;\rightarrow&space;s_{3})

```python
from ordrbook import OrderBook


book = OrderBook()

# B1: BUY 10 LIMIT 99
book.bid({'order_id': 'b1', 'trade_id': 'b1', 'timestamp': 1, 'quantity': 10, 'price': 99.})

# B2: BUY 40 LIMIT 99
book.bid({'order_id': 'b2', 'trade_id': 'b2', 'timestamp': 2, 'quantity': 40, 'price': 99.})

# S1: SELL 30 LIMIT 98 (Match! B1 Gets Priority)
book.ask({'order_id': 's1', 'trade_id': 's1', 'timestamp': 3, 'quantity': 30, 'price': 98.})

# B3: BUY 20 LIMIT 100
book.bid({'order_id': 'b3', 'trade_id': 'b3', 'timestamp': 4, 'quantity': 20, 'price': 100.})

# S2: SELL 20 LIMIT 101 (Price cannot be fulfilled yet. Placed on order book.)
book.ask({'order_id': 's2', 'trade_id': 's2', 'timestamp': 5, 'quantity': 20, 'price': 101.})

# S3: SELL 10 LIMIT 99 (Match! B2 is part-filled.)
book.ask({'order_id': 's3', 'trade_id': 's3', 'timestamp': 6, 'quantity': 10, 'price': 99.})
```

There are two important points to mention, regarding broadcasting the order book publicly:

  1. Neither counterparty can know whom they were matched with. Only the exchange can know this information.
  2. Only the depth can be visible to the public. The individual trade sizes must not be made public.

You can view the order book and/or trades by using the following code:

```python
print('Trades:')

for entry in order_book.tape:
    print(f"`{entry['party1'][0]}` sold {entry['quantity']} @ £{entry['price']} to `{entry['party2'][0]}`")

print('Order Book:')
print('Bids:')

if order_book.bids != None and len(order_book.bids) > 0:
    for key, value in order_book.bids.tree.items(reverse=True):
        print(f'Price: {key}, Volume: {value.volume}')

print('Asks:')

if order_book.asks != None and len(order_book.bids) > 0:
    for key, value in order_book.asks.tree.items():
        print(f'Price: {key}, Volume: {value.volume}')
```

----

### Installation

`pip install ordrbook`
