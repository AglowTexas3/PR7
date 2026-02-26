from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int
    currency: str = "USD"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("currency mismatch")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, qty: int) -> "Money":
        if qty < 0:
            raise ValueError("qty must be non-negative")
        return Money(self.amount * qty, self.currency)
