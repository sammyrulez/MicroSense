from http.client import CREATED
from typing import List
from fastapi import FastAPI, Header, Response, Security
from fastapi.security import APIKeyHeader  
app = FastAPI()   
from microsense import database
from dataclasses import dataclass
from datetime import datetime
import os

MICROSENSE_API_KEY = os.environ.get("MICROSENSE_API_KEY")
if MICROSENSE_API_KEY is None:
    raise ValueError("No MICROSENSE_API_KEY set for API authentication")


api_key_header = APIKeyHeader(name="X-API-Key")
device_serial_number_header = Header("X-Device-Serial-Number")

@app.get("/") 
async def main_route():     
  return {"message": "Hey, It is me Goku"}

@dataclass
class Metric:
   timestamp: datetime
   value: float
   name: str
   device:str
    
@app.post("/metrics")
async def metics( metric:Metric,device_serial_number:str = device_serial_number_header ,api_key_header: str = Security(api_key_header)) -> Response:
    if api_key_header == None or api_key_header != MICROSENSE_API_KEY:
        return Response(content="Invalid API Key", status_code=403, media_type="text/plain") # TODO Refactor function to return a 403 status code
    
    database.insert_metric(metric.timestamp.timestamp(), metric.value,metric.name, metric.device )
    return Response(content="Ok", status_code=CREATED ,media_type="text/plain")

@app.get("/metrics/{metric}")
async def get_metrics(metric:str,api_key_header: str = Security(api_key_header))-> List:
    if api_key_header == None or api_key_header != MICROSENSE_API_KEY:
        return Response(content="Invalid API Key", status_code=403, media_type="text/plain") # TODO Refactor function to return a 403 status code
    
    return database.get_metrics(metric)# TODO return a metric object instead of a tuple