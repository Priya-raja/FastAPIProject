from typing import Any
from fastapi import FastAPI,HTTPException
from scalar_fastapi import get_scalar_api_reference

from schemas import Shipment

app = FastAPI()

   

shipments = {
    12701: {
        "weight": .6,
        "content": "glassware",
        "status": "placed"
    },
    12702: {
        "weight": 2.3,
        "content": "books",
        "status": "shipped"
    },
    12703: {
        "weight": 1.1,
        "content": "electronics",
        "status": "delivered"
    },
    12704: {
        "weight": 3.5,
        "content": "furniture",
        "status": "in transit"
    },
    12705: {
        "weight": .9,
        "content": "clothing",
        "status": "returned"
    },
    12706: {
        "weight": 4.0,
        "content": "appliances",
        "status": "processing"
    },
    12707: {
        "weight": 1.8,
        "content": "toys",
        "status": "placed"
    },
}


@app.get("/shipment/latest")
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())
    return shipments[id]


@app.get("/shipment/{id}")
def get_shipment(id: int) -> dict[str, Any]:

    if id not in shipments:
       
       raise HTTPException(status_code=404, detail="Shipment not found")

    return shipments[id]

# Post a new shipment
@app.post("/shipment")

def submit_shipment(shipment: Shipment) -> dict[str, int]:
    new_id = max(shipments.keys()) + 1
    
    shipments[new_id]={
        "weight": shipment.weight,
        "content": shipment.content,
        "status": "placed"
    }
    return {"id": new_id}

@app.get("/shipment/field/{field}")
def get_shipment_by_field(field: str, id: int) -> dict[str, Any]:

    if id not in shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    if field not in shipments[id]:
        raise HTTPException(status_code=404, detail=f"Field '{field}' not found in shipment {id}")

    return {
        field: shipments[id][field]
    }


@app.put("/shipment")
def update_shipment_status(id: int, content: str, weight: float, status: str) -> dict[str, Any]:

    if id not in shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    shipments[id] = {
        "weight": weight,
        "content": content,
        "status": status
    }
    return shipments[id]

@app.patch("/shipment")
def patch_shipment_status(
    id: int, 
    body: dict[str, Any]) -> dict[str, Any]:

    if id not in shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    shipment = shipments[id]
    shipment.update(body)

    shipments[id] = shipment   

    return shipments[id]

@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    
    if id not in shipments:
        raise HTTPException(status_code=404, detail="Shipment not found")

    del shipments[id]

    return {"detail": f"Shipment {id} deleted successfully"}

# Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )