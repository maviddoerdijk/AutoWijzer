from openai import OpenAI
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
import streamlit as st
from pydantic_models import Car, CarPopulated, UserData
load_dotenv()





def get_car_from_prompt_legacy(user_data):        
    # Initialize OpenAI client
    client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

    # Construct the prompt for the OpenAI API
    prompt = f"""
    Based on the following user data, provide information about a suitable car:
    - Budget: {user_data.get('budget', {}).get('min', 'unknown')} - {user_data.get('budget', {}).get('max', 'unknown')} {user_data.get('budget', {}).get('type', 'unknown')}
    - Fuel Type: {user_data.get('fuel_type', 'unknown')}
    - Battery Range: {user_data.get('battery_range', 'unknown')} km
    - Fast Charging: {user_data.get('fast_charging', 'unknown')}
    - Suitcase Count: {user_data.get('suitcase_count', 'unknown')}
    - Circumstance: {user_data.get('circumstance', 'unknown')}
    
    Please return the car information in the following JSON format:
    {{
        "name": "<Car Name>",
        "price": "<Price>",
        "image": "<Image URL>",
        "dealers": [
            {{
                "name": "<Dealer Name>",
                "link": "<Dealer Link>"
            }},
            ...
        ]
    }}
    """

    # Request completion from the OpenAI API
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Adjust to the appropriate model name if necessary
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}  # Ensure the response is in JSON format
    )

    # Parse the response
    result = completion.choices[0].message.content
    # return as dict
    return json.loads(result)
    
def get_car_from_prompt(user_data: UserData) -> CarPopulated:
    client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])
    prompt = f"""
    Based on the following user data:
    ```
    - Budget: {user_data.budget_min} - {user_data.budget_max} {user_data.budget_type}
    - Fuel Type: {user_data.fuel_type}
    - Battery Range: {user_data.battery_range} km
    - Fast Charging: {user_data.fast_charging}
    - Suitcase Count: {user_data.suitcase_count}
    - Circumstance: {user_data.circumstance}
    ```
    
    Find a car that matches this criteria, and specify all information according to the pydantic model.
    """
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages = [
            {"role": "system", "content": "You are a helpful car expert. Answer in a pydantic format, and do give any car that does not match the criteria."},
            {"role": "user", "content": prompt},
        ],
        response_format=Car
    )
    car_data = completion.choices[0].message.parsed
    unpopulated_car_data = CarPopulated(**car_data.model_dump())
    return unpopulated_car_data

if __name__ == "__main__":
    import random
    def generate_mock_user_data() -> UserData:
        budget_min = random.choice(["10000", "20000", "30000"])
        budget_max = random.choice(["40000", "50000", "60000"])
        budget_type = random.choice(["monthly", "yearly"])
        fuel_type = random.choice(["petrol", "diesel", "electric", "hybrid"])
        battery_range = random.choice(["200km", "300km", "400km"])
        fast_charging = random.choice(["yes", "no"])
        suitcase_count = random.choice(["2", "3", "4"])
        circumstance = random.choice(["city", "highway", "mixed"])
        hybride_type = random.choice(["mild", "full", "plug-in"])
        efficiency = random.choice(["15km/l", "20km/l", "25km/l"])
        fuel_tank_size = random.choice(["40L", "50L", "60L"])

        return UserData(
            budget_min=budget_min,
            budget_max=budget_max,
            budget_type=budget_type,
            fuel_type=fuel_type,
            battery_range=battery_range,
            fast_charging=fast_charging,
            suitcase_count=suitcase_count,
            circumstance=circumstance,
            hybride_type=hybride_type,
            efficiency=efficiency,
            fuel_tank_size=fuel_tank_size
        )
    user_data = generate_mock_user_data()
    car_data = get_car_from_prompt(user_data)
    print(car_data)