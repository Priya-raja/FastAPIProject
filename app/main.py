"""FastAPI application for shipment management."""

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from rich import print, panel
from schemas import ShipmentCreate, ShipmentRead, ShipmentStatus, ShipmentUpdate
from database import Database
from database.session import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # print("[green]Starting up...[/green]")
    # print(panel.Panel("Starting up", border_style="blue"))
    create_db_and_tables()
    yield
    print("[red]Shutting down...[/red]")
    print(panel.Panel("Shutting down", border_style="red"))


app = FastAPI(lifespan=lifespan)

db = Database()
db.connect_to_db()
def _get_shipment_or_404(shipment_id: int) -> dict[str, str | float | int]:
    """Return a shipment record or raise a 404 error if it is missing."""
    shipment = db.get(shipment_id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )
    return shipment


@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(shipment_id: int) -> dict[str, str | float | int]:

   
    """Fetch a single shipment by its identifier."""
    return _get_shipment_or_404(shipment_id)


@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    """Create a new shipment and return its generated identifier."""
    new_id = db.create(shipment)
    # Return id for later use
    return {"id": new_id}


@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(shipment_id: int, body: ShipmentUpdate) -> dict[str, str | float | int]:
    """Update the status of an existing shipment."""
    db.update(shipment_id, body)
    return _get_shipment_or_404(shipment_id)


@app.delete("/shipment")
def delete_shipment(shipment_id: int) -> dict[str, str]:
    """Delete a shipment and confirm the removal."""
    db.delete(shipment_id)
    _get_shipment_or_404(shipment_id)
    
    return {"detail": f"Shipment with id #{shipment_id} is deleted!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs() -> object:
    """Serve the Scalar API documentation page."""
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
