"""An unofficial Python wrapper for the Nexo Pro exchange API v1
.. moduleauthor:: Erwin Lejeune
"""

__version__ = "1.0.1"

from nexo.client import Client
from nexo.response_serializers import (
    AdvancedOrderResponse,
    Balances,
    Orders,
    Pairs,
    Quote,
    TradeHistory,
    Transaction,
    OrderResponse,
    OrderDetails,
)
from nexo.exceptions import (
    NexoAPIException,
    NotImplementedException,
    NexoRequestException,
    NEXO_API_ERROR_CODES,
)
