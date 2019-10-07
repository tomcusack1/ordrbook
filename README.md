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

B1, B2, S1 (Match! B1 Gets Priority), B3, S2, S3 (Match! B2 is part-filled).

### Installation

`conda create -n orderbook python=3.7`

`source activate orderbook`

`pip install -r requirements.txt`

`python setup.py install`

### Sample Usage

```python
from time import time
from uuid import uuid4

from order.app import OrderBook


order_book = OrderBook()

# SELL 100 LIMIT 90
order_book.ask_limit_order({'order_id': str(uuid4()), 'trade_id': str(uuid4()), 'timestamp': int(time()),
                            'type': 'ask', 'quantity': 100, 'price': 90., 'type': 'limit'})

# BUY 1000 LIMIT 100
order_book.bid_limit_order({'order_id': str(uuid4()), 'trade_id': str(uuid4()), 'timestamp': int(time()),
                            'type': 'bid', 'quantity': 1000, 'price': 100.0, 'type': 'limit'})

# SELL 100
order_book.ask_market_order({'order_id': str(uuid4()), 'trade_id': str(uuid4()), 'timestamp': int(time()),
                             'type': 'ask', 'quantity': 100, 'type': 'market'})

# BUY 50
order_book.bid_market_order({'order_id': str(uuid4()), 'trade_id': str(uuid4()), 'timestamp': int(time()),
                             'type': 'bid', 'quantity': 50, 'type': 'market'})
```