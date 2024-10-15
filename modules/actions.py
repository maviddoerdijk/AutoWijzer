from modules.llm.openai_connection import get_car_from_prompt
from modules.scraper.images import get_car_base64

def get_car_data(user_data: dict, return_mock_data: bool = False) -> dict:
    # First, get the basic car data from the OpenAI API
    car_data = get_car_from_prompt(user_data, return_mock_data=return_mock_data)

    # Then, populate the data using webscrapers
    car_image_base64 = get_car_base64(car_data['name'])
    
    car_data['image'] = car_image_base64
    

    return car_data

