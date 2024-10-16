from pydantic import BaseModel
from typing import Optional, List


class Car(BaseModel):
    price: str
    km_range: str
    fuel_type: str
    make: str
    model: str
    full_name: str # add name as last attribute, so AI will give it last
    
class CarDealer(BaseModel):
    provider_full_name: str
    link: str
    
class CarPopulated(Car):
    # contains all attributes that are to populate the class later (after get_car_from_prompt)
    # OPTIONAL
    image: Optional[bytes] = None # base64 encoded image bytes object
    dealers: List[CarDealer] = [] # dealers will later have its own model, for now we let it free
    
class UserData(BaseModel):
    budget_min: Optional[str] = None
    budget_max: Optional[str] = None
    budget_type: Optional[str] = None
    fuel_type: Optional[str] = None
    battery_range: Optional[str] = None
    fast_charging: Optional[str] = None
    suitcase_count: Optional[str] = None
    circumstance: Optional[str] = None
    hybride_type: Optional[str] = None
    efficiency: Optional[str] = None
    fuel_tank_size: Optional[str] = None