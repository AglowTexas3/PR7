from dataclasses import dataclass, field
from typing import List, Tuple
from application.ports import PaymentGateway
from domain.money import Money


@dataclass
class FakePaymentGateway(PaymentGateway):
    charges: List[Tuple[str, Money]] = field(default_factory=list)
    should_fail: bool = False

    def charge(self, order_id: str, amount: Money) -> bool:
        if self.should_fail:
            return False
        self.charges.append((order_id, amount))
        return True
