from dataclasses import dataclass, field
from typing import List
from .order_line import OrderLine
from .order_status import OrderStatus
from .money import Money
from .exceptions import DomainError


@dataclass
class Order:
    id: str
    lines: List[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.NEW

    def add_line(self, line: OrderLine) -> None:
        """После оплаты строки менять нельзя."""
        if self.status == OrderStatus.PAID:
            raise DomainError("cannot modify order after payment")
        self.lines.append(line)

    @property
    def is_empty(self) -> bool:
        return len(self.lines) == 0

    @property
    def total_amount(self) -> Money:
        """Итоговая сумма равна сумме строк (инвариант выполняется за счёт вычисления)."""
        total = Money(0, "USD")
        for line in self.lines:
            total = total + line.line_total
        return total

    def ensure_can_be_paid(self) -> None:
        """Инварианты оплаты: не пустой и не оплачен ранее."""
        if self.is_empty:
            raise DomainError("cannot pay empty order")
        if self.status == OrderStatus.PAID:
            raise DomainError("order already paid")

    def mark_paid(self) -> None:
        """Пометить заказ оплаченным с проверкой инвариантов."""
        self.ensure_can_be_paid()
        self.status = OrderStatus.PAID
