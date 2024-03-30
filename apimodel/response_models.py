import datetime
from enum import Enum
from typing import List, TypeVar

from pydantic import BaseModel

dataType = TypeVar("dataType")

class Status(Enum):
    SUCCESS = "successful",
    FAIL = "fail"
    PARTIAL_SUCCESS = "partially successful"


class APIError(BaseModel):
    status: Status = Status.FAIL.value
    type: str = None
    message: str


class PriceResponse(BaseModel):
    timestamp: datetime.datetime = None
    symbol: str = None
    price: float = None


class StatResponse(BaseModel):
    operation: str=None
    value: float = None














