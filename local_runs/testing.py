import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.actions import get_car_data

def test_1():
    user_data = {
        "budget": {"type": "Maandelijks", "min": 300, "max": 600},
        "fuel_type": "Elektrisch",
        "battery_range": 400,
        "fast_charging": "Ja",
        "suitcase_count": "3 koffers (360 liter)",
        "circumstance": "Milieubewuste rijder"
    }
    car_data = get_car_data(user_data)
    print(car_data)
    
if __name__ == "__main__":
    test_1()