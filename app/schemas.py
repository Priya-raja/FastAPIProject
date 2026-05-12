
from pydantic import BaseModel,Field


class Shipment(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(description="Weight of the shipment (kg)", le=25)
    status: str 