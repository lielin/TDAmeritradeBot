from datetime import datetime

from typing import List
from typing import Union
from typing import Optional


class Trade():

    def __init__(self):
        self.order = {}
        self.trade_id = ""  # Identifier for trade

        self.side = ""
        self.side_opposite = ""
        self.enter_or_exit = ""
        self.enter_or_exit_opposite = ""

        self._order_response = {}
        self._trigger_added = False
        self._multi_leg = False     # Identify multi leg order

    def new_trade(self, trade_id: str, order_type: str, side: str, enter_or_exit: str, price: float = 0.00, stop_limit_price: float = 0.00) -> dict:

        self.trade_id = trade_id

        self.order_types = {
            'mkt': 'MARKET',
            'lmt': 'LIMIT',
            'stop': 'STOP',
            'stop_lmt': 'STOP_LIMIT',
            'trailing_stop': 'TRAILING_STOP'
        }

        self.order_instructions = {
            'enter': {
                'long': 'BUY',
                'short': 'SELL_SHORT'
            },
            'exit': {
                'long': 'SELL',
                'short': 'BUY_TO_COVER'
            }
        }

        self.order = {
            "orderStrategyType": "SINGLE",
            "orderType": self.order_types[order_type],
            "session": "NORMAL",
            "duration": "DAY",
            "orderLegCollection": [
                {
                    "instruction": self.order_instructions[enter_or_exit][side],
                    "quantity": 0,
                    "instrument": {
                        "symbol": None,
                        "assetType": None
                    }
                }
            ]
        }

        # Modify key based on what's given
        if self.order['orderType'] == 'STOP':
            self.order['stopPrice'] = price

        elif self.order['orderType'] == 'LIMIT':
            self.order['price'] = price

        elif self.order['orderType'] == 'STOP_LIMIT':
            self.order['price'] = stop_limit_price
            self.order['stopPrice'] = price

        elif self.order['orderType'] == 'TRAILING_STOP':
            self.order['stopPriceLinkBasis'] = ""
            self.order['stopPriceLinkType'] = ""
            self.order['stopPriceOffset'] = 0.00
            self.order['stopType'] = 'STANDARD'

        # Make a reference to the side we take, useful when adding other components.
        self.enter_or_exit = enter_or_exit
        self.side = side
        self.order_type = order_type
        self.price = price

        # If it's a stop limit order or stop order, set the stop price.
        if self.is_stop_order or self.is_stop_limit_order:
            self.stop_price = price
        else:
            self.stop_price = 0.0

        # If it's a stop limit order set the stop limit price.
        if self.is_stop_limit_order:
            self.stop_limit_price = stop_limit_price
        else:
            self.stop_limit_price = 0.0

        # If it's a limit price set the limit price.
        if self.is_limit_order:
            self.limit_price = price
        else:
            self.limit_price = 0.0

        # Set the enter or exit state.
        if self.enter_or_exit == 'enter':
            self.enter_or_exit_opposite = 'exit'
        if self.enter_or_exit == 'exit':
            self.enter_or_exit_opposite = 'enter'

        # Set the side state.
        if self.side == 'long':
            self.side_opposite = 'short'
        if self.side == 'short':
            self.side_opposite = 'long'

        return self.order