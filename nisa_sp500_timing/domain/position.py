class Sp500Position:
    def __init__(self, total_quantity: float, avg_cost: float, account_type: str = "NISA"):
        self.total_quantity = total_quantity
        self.avg_cost = avg_cost
        self.account_type = account_type

    def market_value(self, current_price: float) -> float:
        return self.total_quantity * current_price

    def unrealized_pnl(self, current_price: float) -> float:
        return self.total_quantity * (current_price - self.avg_cost)
