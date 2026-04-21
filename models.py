from pydantic import BaseModel

class UserAccountContext(BaseModel):
    customer_id: int
    name: str
    allergies: list


class InputGuardRailOutput(BaseModel):
    is_off_topic: bool
    reason: str
