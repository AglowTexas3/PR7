import pytest

from domain.money import Money
from domain.order import Order
from domain.order_line import OrderLine
from domain.order_status import OrderStatus
from domain.exceptions import DomainError

from application.pay_order_use_case import PayOrderUseCase
from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway


def create_sample_order(order_id: str = "o1") -> Order:
    line1 = OrderLine(product_id="p1", qty=2, price=Money(50))
    line2 = OrderLine(product_id="p2", qty=1, price=Money(100))
    return Order(id=order_id, lines=[line1, line2])


def test_successful_payment():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = create_sample_order("o1")
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)
    result = use_case.execute("o1")

    assert result is True
    assert order.status == OrderStatus.PAID
    assert len(gateway.charges) == 1
    charged_order_id, charged_amount = gateway.charges[0]
    assert charged_order_id == "o1"
    assert charged_amount.amount == order.total_amount.amount


def test_error_on_empty_order():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    empty_order = Order(id="o2", lines=[])
    repo.save(empty_order)

    use_case = PayOrderUseCase(repo, gateway)

    with pytest.raises(DomainError):
        use_case.execute("o2")


def test_error_on_second_payment():
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    order = create_sample_order("o3")
    order.mark_paid()
    repo.save(order)

    use_case = PayOrderUseCase(repo, gateway)

    with pytest.raises(DomainError):
        use_case.execute("o3")


def test_cannot_modify_after_payment():
    order = create_sample_order("o4")
    order.mark_paid()

    with pytest.raises(DomainError):
        order.add_line(OrderLine(product_id="p3", qty=1, price=Money(10)))


def test_total_sum_is_sum_of_lines():
    order = create_sample_order("o5")
    expected = sum(line.line_total.amount for line in order.lines)
    assert order.total_amount.amount == expected
