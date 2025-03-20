import datetime
from typing import Any, List, Dict
import numpy as np
import talib  # type: ignore

from investfly.models import *
from investfly.utils import *


# This sample show how you can use pandas_ta module at https://github.com/twopirllc/pandas-ta
# to compute implement your own custom indicator
# This indicator computes RSI of SMA - it computes SMA and uses it as input to RSI.


class RsiOfSma(Indicator):

    def getIndicatorSpec(self) -> IndicatorSpec:
        # In this method, you must construct and return IndicatorSpec object that specifies
        # indicator name, description and any parameters it needs. Stanard parameters like (barinterval, count, lookback)
        #  are automatically added
        indicator = IndicatorSpec("RSI of SMA")
        indicator.addParam("sma_period", IndicatorParamSpec(ParamType.INTEGER, True, 5, IndicatorParamSpec.PERIOD_VALUES))
        indicator.addParam("rsi_period", IndicatorParamSpec(ParamType.INTEGER, True, 10, IndicatorParamSpec.PERIOD_VALUES))
        return indicator

    def getDataSourceType(self) -> DataSource:
        return DataSource.BARS

    def computeSeries(self, params: Dict[str, Any], bars: List[Bar]) -> List[DatedValue]:
        dates, close = CommonUtils.extractCloseSeries(bars)
        sma_period = params['sma_period']
        smaSeries = talib.SMA(np.array(close), timeperiod=sma_period)
        rsi_period = params['rsi_period']
        rsiSeries = talib.RSI(smaSeries, timeperiod=rsi_period)
        return CommonUtils.createListOfDatedValue(dates, rsiSeries)



