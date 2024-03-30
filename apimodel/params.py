from enum import Enum


class Symbols(str, Enum):
    BTCUSDT = "BTCUSDT"
    DOGEUSDT = "DOGEUSDT"
    LTCUSDT = "LTCUSDT"


class Analysis(str, Enum):
    AVERAGE = "Average"
    MEDIAN = "Median"
    STD_DEVIATION = "Standard Deviation"
    PCTG_CHG = 'Percentage Change'
