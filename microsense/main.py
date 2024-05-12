from http.client import CREATED
from typing import List
from fastapi import FastAPI, Response  
app = FastAPI()   
from microsense import database
from dataclasses import dataclass
from datetime import datetime

@app.get("/") 
async def main_route():     
  return {"message": "Hey, It is me Goku"}

@dataclass
class Metric:
   timestamp: datetime
   value: float
   name: str
    
@app.post("/metrics")
async def metics( metric:Metric) -> Response:
    database.insert_metric(metric.timestamp.timestamp(), metric.value,metric.name )
    return Response(content="Ok", status_code=CREATED ,media_type="text/plain")

@app.get("/metrics/{metric}")
async def get_metrics(metric:str)-> List:
    return database.get_metrics(metric)