from typing import List
from modules.pydantic_models import CarDealer

car_sites_config = {
    'Auto Scout 🚖': 'https://www.autoscout24.nl/lst/{make}/{model_formatted_hyphens}',
    'Auto Track 🛣️': 'https://www.autotrack.nl/elektrische-auto/{make}/{model_formatted_hyphens}',
    'Gas Pedaal 💰': 'https://www.gaspedaal.nl/{make}/{model_formatted_hyphens}',
    'Auto Trader 🚗': 'https://www.autotrader.nl/auto/{make}/{model_formatted_hyphens}/',
    'Via Bovag 🚙': 'https://www.viabovag.nl/auto/merk-{make}/model-{model_formatted_hyphens}',
}
# provider_name : unformatted_f_string

def get_car_dealers_data(make: str, model: str, full_name: str) -> List[CarDealer]:
    model_formatted_hyphens = model.replace(' ', '-')
    car_dealers = []
    
    for provider_name, provider_url in car_sites_config.items():
        car_dealers.append(CarDealer(
            provider_full_name=provider_name,
            link=provider_url.format(make=make, model_formatted_hyphens=model_formatted_hyphens)
        ))
    return car_dealers