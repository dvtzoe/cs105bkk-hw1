"""HW1: a Bangkok food-delivery order. Practises Sessions 1-3: aliasing and defaults, comprehensions,
classes with a guarded property, __repr__ and __eq__, inheritance with super(), composition and duck typing."""

from typing import override


class MenuItem:
    """A dish on a restaurant's menu. The price is a whole number of baht."""

    def __init__(self, name: str, price: int):
        """Store the name and the price. The price goes through the setter, so it is checked."""

        self._price: int
        self.price = price

        self.name: str = name

    @property
    def price(self) -> int:
        """Provided: the price in baht."""

        return self._price

    @price.setter
    def price(self, value: int) -> None:
        """Set the price. Raise ValueError if it is 0 or less, and keep the old price."""

        if value <= 0:
            raise ValueError(f"price must be more than 0 baht, got {value}")

        self._price = value

    @override
    def __repr__(self) -> str:
        """Return the developer view, for example MenuItem('Pad Thai', 60)."""

        return f"MenuItem({self.name!r}, {self.price})"

    @override
    def __eq__(self, other: object) -> bool:
        """Two menu items are equal when their names and prices are equal."""

        if not isinstance(other, self.__class__):
            raise NotImplementedError

        return self.name == other.name and self.price == other.price

    def cost(self, quantity: int) -> int:
        """Provided: what quantity of this dish costs, in baht."""

        return self.price * quantity


class PromoItem(MenuItem):
    """A dish on a "buy 2, get 1 free" promotion: every third one is free."""

    def __init__(self, name: str, price: int):
        super().__init__(name, price)

    @override
    def cost(self, quantity: int) -> int:
        """Return what quantity costs when every third one is free."""

        return self.price * (quantity - (quantity // 3))


class Order:
    """One customer's delivery order: a list of (menu item, quantity) lines."""

    # Provided: baht added to every order with food in it
    delivery_fee: int = 30

    # Provided: food worth this much or more is delivered free
    free_delivery_from: int = 300

    def __init__(self, customer: str, lines: list[tuple[MenuItem, int]] | None = None):
        """Store the customer and a new list of lines. Never share a list with the caller or another order."""

        self.customer: str = customer

        self.lines: list[tuple[MenuItem, int]]
        if lines is None:
            self.lines = []
        else:
            self.lines = lines.copy()

    def add(self, item: MenuItem, quantity: int = 1) -> None:
        """Add one line. Raise ValueError if quantity is less than 1."""

        if quantity <= 0:
            raise ValueError(f"quantity must be at least 1, got {quantity}")

        self.lines.append((item, quantity))

    def total(self) -> int:
        """Return the food cost plus the delivery fee; free delivery from free_delivery_from; 0 if empty."""

        cum_cost = sum(menu_item.cost(quantity) for menu_item, quantity in self.lines)

        if cum_cost < self.free_delivery_from:
            cum_cost += self.delivery_fee

        return cum_cost

    def summary(self) -> list[str]:
        """Return one text line per order line, for example "2 x Pad Thai"."""

        return [f"{quantity} x {item.name}" for item, quantity in self.lines]


def cheapest(options: list[Order]) -> object | None:
    """Return the option with the smallest total(). First one wins a tie; None for an empty list.

    An option can be anything with a total() method, not only an Order.
    """

    return min(options, default=None, key=lambda order: order.total())
