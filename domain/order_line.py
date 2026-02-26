from dataclasses import dataclass
from .money import Money


@dataclass
class OrderLine:
    product_id: str
    qty: int
    price: Money

    @property
    def line_total(self) -> Money:
        return self.price * self.qty
