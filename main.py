from random import randint
from fastapi import FastAPI
from datetime import datetime
from fastapi import HTTPException
from fastapi import Response
from typing import Any

app = FastAPI(root_path="/api/v1")


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


sample_data = [
    {
        "campaign_id": 1,
        "name": "Campaign 1",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    },
    {
        "campaign_id": 2,
        "name": "Campaign 2",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    },
    {
        "campaign_id": 3,
        "name": "Campaign 3 ",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    }
]

"""
Campaigns
- campaign_id
- name
- due_date
- created_at
"""


@app.get("/campaigns")
async def get_campaigns():
    return {"campaigns": sample_data}


@app.get("/campaigns/{campaign_id}")
async def read_campaign(campaign_id: int):
    for campaign in sample_data:
        if campaign["campaign_id"] == campaign_id:
            return campaign
    raise HTTPException(status_code=404)


@app.post("/campaigns", status_code=201)
async def create_campaign(body: dict[str, Any]):
    new: Any = {
        "campaign_id": randint(1, 1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now()
    }
    sample_data.append(new)
    return new


@app.put("/campaigns/{id}")
async def update_campaign(id: int, body: dict[str, Any]):
    for index, campaign in enumerate(sample_data):
        if campaign["campaign_id"] == id:
            updated: Any = {
                "campaign_id": id,
                "name": body.get("name"),
                "due_date": body.get("due_date"),
                "created_at": campaign.get("created_at")
            }
            sample_data[index] = updated
            return updated
    raise HTTPException(status_code=404)


@app.delete("/campaigns/{id}")
async def delete_campaign(id: int):
    for index, campaign in enumerate(sample_data):
        if campaign["campaign_id"] == id:
            sample_data.pop(index)
            return Response(status_code=204)

    raise HTTPException(status_code=404)
