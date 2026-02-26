from enum import Enum


class OrderStatus(str, Enum):
    NEW = "NEW"
    PAID = "PAID"
