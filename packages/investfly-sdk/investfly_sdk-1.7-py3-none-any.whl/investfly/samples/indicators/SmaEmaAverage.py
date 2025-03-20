from typing import Any, List, Dict

import numpy as np
import talib  # type: ignore

from investfly.models import *
from investfly.utils import *

# This sample show how you can use pandas_ta module at https://github.com/twopirllc/pandas-ta
# to compute over 100 technical indicators
# This indicator computes average of SMA and EMA for given period

class SmaEmaAverage(Indicator):

    def getIndicatorSpec(self) -> IndicatorSpec:
        # In this method, you must construct and return IndicatorSpec object that specifies
        # indicator name, description and any parameters it needs. Stanard parameters like (barinterval, count, lookback)
        #  are automatically added
        indicator = IndicatorSpec("SMA EMA Average")
        indicator.addParam('period', IndicatorParamSpec(ParamType.INTEGER, True, 5, IndicatorParamSpec.PERIOD_VALUES))
        return indicator

    def getDataSourceType(self) -> DataSource:
        return DataSource.BARS


    def computeSeries(self, params: Dict[str, Any], bars: List[Bar]) -> List[DatedValue]:
        # Load the bars into Pandas dataframe
        dates, close = CommonUtils.extractCloseSeries(bars)
        # Get supplied period
        period = params['period']
        # Call pandas_ta module to compute sma and ema
        # see https://github.com/twopirllc/pandas-ta
        smaSeries = talib.SMA(np.array(close), timeperiod=period)
        emaSeries = talib.EMA(np.array(close), timeperiod=period)
        avgSeries = (smaSeries + emaSeries) / 2
        return CommonUtils.createListOfDatedValue(dates, avgSeries)
