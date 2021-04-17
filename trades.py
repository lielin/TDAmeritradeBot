from datetime import datetime

from typing import List
from typing import Union
from typing import Optional


class Trade():

    # Initializes a new order
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

    def to_dict(self) -> dict:

        # Initialize the Dict.
        obj_dict = {
            "__class___": self.__class__.__name__,
            "__module___": self.__module__
        }

        # Add the Object.
        obj_dict.update(self.__dict__)

        return obj_dict

    # Creates new Trade object
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

    # Adds an instrument to trade
    def instrument(self, symbol: str, quantity: int, asset_type: str, sub_asset_type: str = None,
                   order_leg_id: int = 0) -> dict:

        leg = self.order['orderLegCollection'][order_leg_id]

        leg['instrument']['symbol'] = symbol
        leg['instrument']['assetType'] = asset_type
        leg['quantity'] = quantity

        self.order_size = quantity
        self.symbol = symbol
        self.asset_type = asset_type

        return leg

    # Adds an Option instrument to the Trade object
    def add_option_instrument(self, symbol: str, quantity: int, order_leg_id: int = 0) -> dict:
        self.instrument(
            symbol=symbol,
            quantity=quantity,
            asset_type='OPTION',
            order_leg_id=order_leg_id
        )

        leg = self.order['orderLegCollection'][order_leg_id]

        return leg

    # Converts order to 'Good Till Cancel' order.
    def good_till_cancel(self, cancel_time: datetime) -> None:

        self.order['duration'] = 'GOOD_TILL_CANCEL'
        self.order['cancelTime'] = cancel_time.isoformat()

    # Modifies the side the order takes.
    def modify_side(self, side: str, leg_id: int = 0) -> None:

        # Validate the Side.
        if side and side not in ['buy', 'sell', 'sell_short', 'buy_to_cover', 'sell_to_close', 'buy_to_open']:
            raise ValueError(
                "The side you have specified is not valid. Please choose a valid side: ['buy', 'sell', 'sell_short', "
                "'buy_to_cover','sell_to_close', 'buy_to_open'] "
            )

        # Set the Order.
        if side:
            self.order['orderLegCollection'][leg_id]['instruction'] = side.upper()
        else:
            self.order['orderLegCollection'][leg_id]['instruction'] = self.order_instructions[self.enter_or_exit][
                self.side_opposite]

    def add_box_range(self, profit_size: float = 0.00, stop_size: float = 0.00,
                      stop_percentage: bool = False, profit_percentage: bool = False,
                      stop_limit: bool = False, make_one_cancels_other: bool = True,
                      limit_size: float = 0.00, limit_percentage: bool = False):

        if not self._triggered_added:
            self._convert_to_trigger()

            # Add a take profit Limit order.
        self.add_take_profit(
            profit_size=profit_size,
            percentage=profit_percentage
        )

        # Add a stop Loss Order.
        if not stop_limit:
            self.add_stop_loss(
                stop_size=profit_size,
                percentage=stop_percentage
            )
        else:
            self.add_stop_limit(
                stop_size=profit_size,
                limit_size=limit_size,
                stop_percentage=stop_percentage,
                limit_percentage=limit_percentage
            )

        if make_one_cancels_other:
            self.add_one_cancels_other()

        self.is_box_range = True

    def add_stop_loss(self):
        pass

    def add_stop_limit(self):
        pass

    def _calculate_new_price(self):
        pass

    def grab_price(self):
        pass

