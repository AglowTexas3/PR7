from dataclasses import dataclass
from domain.exceptions import DomainError
from application.ports import OrderRepository, PaymentGateway


@dataclass
class PayOrderUseCase:
    order_repository: OrderRepository
    payment_gateway: PaymentGateway

    def execute(self, order_id: str) -> bool:
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            raise DomainError("order not found")

        # доменные инварианты перед вызовом платёжки
        order.ensure_can_be_paid()

        amount = order.total_amount
        success = self.payment_gateway.charge(order.id, amount)
        if not success:
            raise DomainError("payment failed")

        # доменная операция оплаты
        order.mark_paid()
        self.order_repository.save(order)

        return True
