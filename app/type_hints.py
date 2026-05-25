"""Module for type hints and City class definition."""


class City:
    """Represent a city and its population."""

    def __init__(self, name: str, population: int) -> None:
        """Initialize a city instance."""
        self.name = name
        self.population = population


text: str = "Hello, World!"
pert: int = 90
temp: float = 37.5
digits: list[int] = [1, 2, 3, 4, 5]
number: int | float = 3.4

table_1: tuple[int, ...] = (1, 2, 3, 4, 5)
table_2: tuple[float, ...] = (1.1, 2.2, 3.3)

hampshire = City("Hampshire", 1500000)

city_temp: tuple[City, float] = (hampshire, 25.5)

shipment: dict[str, str | int] = {
    "content": "Wooden Table",
    "status": "In Transit",
}
# Can use classes also as hints


def root(num: int | float) -> float:
    """Return the square root of the provided number."""
    return pow(num, 0.5)


root_25 = root(8.4)
