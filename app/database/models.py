from sqlmodel import SQLModel,Field
from enum import Enum
from datetime import datetime
from typing import Optional


class ShipmentStatus(str, Enum):
    """Allowed lifecycle states for a shipment."""

    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class Shipment(SQLModel):
    __tablename__ = "shipment"

    id: Optional[int] = Field(default = None, primary_key=True)
    content: str
    weight: float = Field(description="Weight of the shipment (kg)", le=25)
    status: ShipmentStatus = Field(default = ShipmentStatus.placed)
    destination: int
    estimated_delivery: datetime = Field(description="Estimated delivery date")





