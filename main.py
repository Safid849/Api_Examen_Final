import numbers
from http.client import responses

from fastapi import FastAPI
import base64
from typing import List
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

app = FastAPI()

class Phone(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristic:{
        "ram_memory": int,
        "rom_memory": numbers
    }

list_phone: List[Phone]=[]

@app.get("/health", status_code=200)
async def health():
    return {"Ok"}


@app.post("/phone")
async def post_phone(new_phones: List[Phone]):
    list_phone.extend(new_phones)
    serialized_post = serialize_posts()
    return JSONResponse(content=serialized_post, status_code=201,media_type="application/json")

def serialize_posts():
    post_serialized = []
    for p in list_phone:
        post_serialized.append(p.model_dump())
    return post_serialized

@app.get("/phones")
async def get_phones():
    return list_phone

@app.get("/phones/{identifier}")
async def get_phone(identifier: str):
    for phone in list_phone:
        if phone.identifier == identifier:
            return JSONResponse(content=phone.model_dump(), status_code=200,media_type="application/json")
        else:
            return Response(content=f"phone with identifier {identifier} is not exist",status_code=404, media_type="text/plain")


@app.put("/phones/{id}/characteristics")
async def put_phone(id: str, characteristic: dict):
    for phone in list_phone:
        if phone.identifier == id:
            phone.characteristic = characteristic
            return JSONResponse(content=phone.model_dump(), status_code=200,media_type="application/json")