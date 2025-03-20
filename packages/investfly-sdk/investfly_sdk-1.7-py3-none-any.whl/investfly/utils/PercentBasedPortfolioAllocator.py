from typing import List

from investfly.models.PortfolioModels import Portfolio, PositionType, TradeOrder, TradeType
from investfly.models.StrategyModels import PortfolioSecurityAllocator, TradeSignal


class PercentBasedPortfolioAllocator(PortfolioSecurityAllocator):

    BROKER_FEE = 1.0

    def __init__(self, percent: float) -> None:
        self.percent = percent

    def allocatePortfolio(self, portfolio: Portfolio, tradeSignals: List[TradeSignal]) -> List[TradeOrder]:

        openPositionSecurities = {p.security for p in portfolio.openPositions}
        pendingOrdersSecurities = {o.security for o in portfolio.pendingOrders}
        openAndPendingSecurities = openPositionSecurities.union(pendingOrdersSecurities)

        tradeOrders: List[TradeOrder] = []

        buyingPower = portfolio.balances.buyingPower
        portfolioValue = portfolio.balances.currentValue
        allocatedAmountPerSecurity = (self.percent/100) * portfolioValue

        while buyingPower > allocatedAmountPerSecurity and len(tradeSignals) > 0:
            tradeSignal = tradeSignals.pop(0)
            if tradeSignal.security not in openAndPendingSecurities:
                tradeType = TradeType.BUY if tradeSignal.position == PositionType.LONG else TradeType.SHORT
                tradeOrder = TradeOrder(tradeSignal.security, tradeType, maxAmount=allocatedAmountPerSecurity)
                tradeOrders.append(tradeOrder)
                buyingPower = buyingPower - allocatedAmountPerSecurity - PercentBasedPortfolioAllocator.BROKER_FEE

        return tradeOrders