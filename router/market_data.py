import datetime
from exceptions.custom_exceptions import ItemNotFoundException
from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy import and_
from sqlalchemy.orm import Session
from apimodel.response_models import PriceResponse, StatResponse
from common.database.db_session import get_db
from common.database.market_data import MarketData
from services.db_crud_operations import  retrieve
from apimodel.params import Symbols, Analysis
import statistics
import pandas as pd
from services.datetime_validation import validate_start_end_relativity
router = APIRouter()
import common.global_variables

@router.get("/latest", response_model=PriceResponse)
def get_latest_data(symbol: Symbols = Symbols.BTCUSDT, db: Session = Depends(get_db)):
    """
    Fetch latest of a specific symbol
    :param symbol: symbol to query
     ***Return*** : The latest price of the symbol
     Example:
        Request {symbol: "BTCUSDT"}
        Response {
                  "timestamp": "2024-03-30T11:51:29",
                  "symbol": "BTCUSDT",
                  "price": 69942
                }
    """
    last_logged_timestamp = common.global_variables.current_symbol_prices[symbol]["time"]
    # use caching for improved performance
    if (datetime.datetime.now()-last_logged_timestamp)<datetime.timedelta(minutes=1):
        return PriceResponse(timestamp=last_logged_timestamp, symbol=symbol+"F", price=common.global_variables.current_symbol_prices[symbol]["price"])
    filters = and_( MarketData.symbol == symbol)
    selected_fields = [MarketData.timestamp,  MarketData.price]
    result = retrieve(db, filters, selected_fields)[0]
    if not result:
        raise ItemNotFoundException()
    result = result[0]
    return PriceResponse(timestamp=result.timestamp, symbol=symbol, price=result.price)


@router.get("/history", response_model=PriceResponse)
def get_historical_data(timestamp: datetime.datetime = Query(...),  symbol: Symbols = Symbols.BTCUSDT, db: Session = Depends(get_db)):
    """
    Fetch price of a specific symbol at a given time in history
    :param symbol: symbol to query
    :param timestamp: timestamp to query
     ***Return*** : The price of the given symbol at the given timestamp
     Example:
        Request {symbol: "BTCUSDT", timestamp :"2024-03-30 11:49:50"}
        Response {
                  "timestamp": "2024-03-30T11:49:50",
                  "symbol": "BTCUSDT",
                  "price": 69943
                }
    """
    filters = and_(MarketData.timestamp == timestamp, MarketData.symbol == symbol)
    selected_fields = [MarketData.timestamp, MarketData.price]
    result = retrieve(db, filters, selected_fields)[0]
    if not result:
        raise ItemNotFoundException()
    result = result[0]
    return PriceResponse(timestamp=result.timestamp, symbol=symbol, price=result.price)


@router.get("/statistical_operation", response_model=StatResponse)
def get_statistical_oprations(start_timestamp: datetime.datetime = Query(...), end_timestamp: datetime.datetime = Query(...),
                        symbol: Symbols = Symbols.BTCUSDT,analysis: Analysis = Header(Analysis.AVERAGE), db: Session = Depends(get_db)):
    """
    Perform statistical operations on the specific data
    :param symbol: symbol to query
    :param start_timestamp: date range start time
    :param end_timestamp: date range end time
    :param analysis: which statistical operation to carry out
     ***Return*** : The value of the statistical operation of the given symbol's prices during the given time frame
     Example:
        Request {symbol: "BTCUSDT", start_timestamp :"2024-03-30 11:49:50",
                          end_timestamp :"2024-03-30 11:51:50", analysis: "AVERAGE"}
        Response {
                      "operation": "Average",
                      "value": 69942
                    }
    """
    validate_start_end_relativity(start_timestamp, end_timestamp)
    filters = and_(MarketData.timestamp >= start_timestamp, MarketData.timestamp<=end_timestamp, MarketData.symbol == symbol)
    selected_fields = [MarketData.price]
    result = retrieve(db, filters, selected_fields)[0]
    if not result:
        raise ItemNotFoundException()
    if analysis == Analysis.AVERAGE:
        return StatResponse(operation=analysis, value=statistics.mean(result[0]))
    if analysis == Analysis.MEDIAN:
        return StatResponse(operation=analysis, value=statistics.median(result[0]))
    if analysis == Analysis.STD_DEVIATION:
        return StatResponse(operation=analysis, value=statistics.stdev(result[0]))
    if analysis == Analysis.PCTG_CHG:
        price_series = pd.Series(result[0])
        return StatResponse(operation=analysis, value=price_series.pct_change())

