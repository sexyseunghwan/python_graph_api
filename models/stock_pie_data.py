from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class StockPieData:
    total_stock_amount_krw: Decimal
    stock_names: list[str] = field(default_factory=list)
    stock_amount_krw: list[Decimal] = field(default_factory=list) 
