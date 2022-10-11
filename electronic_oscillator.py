import math

PI = math.pi


class ElectronicOscillator:
    def __init__(self, maximal_charge: float, period: float) -> None:
        self.maximal_charge = maximal_charge
        self.period = period

        self.timer: float = 0

    def work(self):
        self.add_time()

    def add_time(self):
        self.timer += 0.02 # Т.к. обнвление кадра происходит 20 раз в сек. добаляем 1 / 20

    @property
    def charge(self):
        return self.maximal_charge * math.cos(self.cyclic_frequency * self.timer)

    @property
    def amperage(self):
        return -self.maximal_amerage * math.sin(self.cyclic_frequency * self.timer)

    @property
    def maximal_amerage(self):
        return self.cyclic_frequency * self.maximal_charge

    @property
    def cyclic_frequency(self):
        return 2 * PI / self.period
