from pydantic import BaseModel

class UserAccountContext(BaseModel):
    customer_id: int
    name: str
    allergies: list


class InputGuardRailOutput(BaseModel):
    is_off_topic: bool
    reason: str

class RestaurantOutputGuardRailOuput(BaseModel):
    contains_off_topic: bool
    contains_sensitive_info: bool
    reason: str
    
