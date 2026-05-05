from typing import Tuple, List, Dict, Union, Any

class City:
    def __init__(self, name: str, population: int):
        self.name = name
        self.population = population

text:str = "Hello, World!"
pert: int = 90
temp: float = 37.5
digits: list[int] = [1, 2, 3, 4, 5]
number : int | float = 3.4



table_1: tuple[int, ...] = (1, 2, 3, 4, 5)
table_2: tuple[float, ...] = (1.1, 2.2, 3.3)

hampshire = City('Hampshire', 1500000)

city_temp: tuple[City, float] = (hampshire, 25.5)

shipment: dict[str, str | int] ={
    "content": "Wooden Table",
    "status": "In Transit",
}
# Can use classes also as hints




def root(num:int | float) -> float:
    return pow(num, .5)


root_25 = root(8.4)