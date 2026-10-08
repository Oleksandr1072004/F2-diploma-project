# services/price_calculator.py

class PriceCalculator:
    """Калькулятор вартості послуг"""

    def __init__(self):
        self.base_prices = {
            "diagnostics": 500,
            "key_registration": 800,
            "optics_polish": 600,
            "firmware_ecu": 1500,
            "alarm_install": 3000,
            "usa_eu": 2000,
        }

        self.car_multipliers = {
            "economy": 1.0,  # ВАЗ, Daewoo, Chevrolet
            "middle": 1.3,  # Toyota, Honda, VW, Ford
            "premium": 1.8,  # BMW, Mercedes, Audi
            "luxury": 2.5,  # Porsche, Range Rover
        }

    def calculate(self, service: str, car_class: str) -> int:
        base = self.base_prices.get(service, 0)
        multiplier = self.car_multipliers.get(car_class, 1.0)
        return int(base * multiplier)