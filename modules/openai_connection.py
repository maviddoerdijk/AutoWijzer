from pydantic import BaseModel
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
load_dotenv()


# Define the Pydantic model for the car information
class Dealer(BaseModel):
    name: str
    link: str

class CarInfo(BaseModel):
    name: str
    price: str
    image: str
    dealers: list[Dealer]



def get_car_from_prompt(user_data, return_mock_data=False):
    if return_mock_data:
        # Return mock data if requested
        return {
            "name": "Tesla Model 3 !!",
            "price": "€ 45.000",
            "image": "car.png",
            "dealers": [
                {"name": "Autodealer 1", "link": "https://example.com/dealer1"},
                {"name": "Autodealer 2", "link": "https://example.com/dealer2"},
                {"name": "Autodealer 3", "link": "https://example.com/dealer3"}
            ]
        }
        
    # Initialize OpenAI client
    client = OpenAI()

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
    print("PROMPT: ", prompt)

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


if __name__ == "__main__":
    mock_user_data = {
        "budget": {"type": "Maandelijks", "min": 300, "max": 600},
        "fuel_type": "Elektrisch",
        "battery_range": 400,
        "fast_charging": "Ja",
        "suitcase_count": "3 koffers (360 liter)",
        "circumstance": "Milieubewuste rijder"
    }
    car_info = get_car_prompt(user_data=mock_user_data)
    print(car_info)
