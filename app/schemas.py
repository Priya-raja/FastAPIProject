"""Pydantic schemas and status values for shipment data."""

from enum import Enum

from pydantic import BaseModel, Field


class BaseShipment(BaseModel):
    """Shared shipment fields used by request and response models."""

    content: str = Field(max_length=30)
    weight: float = Field(description="Weight of the shipment (kg)", le=25)
    destination: int = Field(description="ID of the destination")


class ShipmentStatus(str, Enum):
    """Allowed lifecycle states for a shipment."""

    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class ShipmentRead(BaseShipment):
    """Response model for returning complete shipment details."""

    status: ShipmentStatus


class ShipmentCreate(BaseShipment):
    """Request model for creating a shipment."""

    pass

class ShipmentUpdate(BaseModel):
    """Request model for changing shipment status."""

    status: ShipmentStatus
