from fastapi import APIRouter, HTTPException, UploadFile, Form,Body
from fastapi.responses import StreamingResponse,FileResponse, Response
import io
import base64
from service.service import ApexService
router = APIRouter()
service = ApexService()


@router.get('/hello')
def analyze():
    return "hello"

@router.post('/add')
def add(name: str=Body(...), img: str= Body(...)):
    # with open(r"C:\Users\ayush.rawat08\Downloads\OIP.jpg", "rb") as image_file:
    #   image_data = image_file.read()
    #   encoded_string = base64.b64encode(image_data).decode("utf-8")
    return service.apexAdd(name,img)

@router.get('/getAll')
def getAll():
    return service.getAll()
   