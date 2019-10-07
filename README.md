# A Python Implementation of a Limit Order Book

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