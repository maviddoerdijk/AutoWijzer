from modules.llm.openai_connection import get_car_from_prompt
from modules.scraper.images import get_car_base64
from modules.pydantic_models import UserData, CarPopulated
from modules.scraper.car_sites import get_car_dealers_data

def get_car_data(user_data: UserData) -> CarPopulated:
    # First, get the basic car data from the OpenAI API
    car_data = get_car_from_prompt(user_data)

    # Then, populate the data using webscrapers
    car_image_base64 = get_car_base64(car_data.full_name)
    car_data.image = car_image_base64
    
    car_dealers_data = get_car_dealers_data(car_data.make, car_data.model, car_data.full_name)  # list of CarDealer objects
    car_data.dealers = car_dealers_data 

    return car_data