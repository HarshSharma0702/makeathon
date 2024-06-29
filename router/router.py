from fastapi import APIRouter, HTTPException, UploadFile, Form,Body
from typing import Optional
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
def add(name: str=Body(...), img: str= Body(...), img2: Optional[str] = Body(None)):
    # with open(r"C:\Users\nishu\Downloads\OIP.jpeg", "rb") as image_file:
    #   image_data = image_file.read()
    # with open(r"C:\Users\nishu\Downloads\P.jpeg", "rb") as image_file:
    #   image_data2 = image_file.read()
    # encoded_string = base64.b64encode(image_data).decode("utf-8")
    # encoded_string2 = base64.b64encode(image_data2).decode("utf-8")
    # return service.apexAdd(name,img)
    return service.apexAdd(name,img, img2)

@router.get('/getAll')
def getAll():
    return service.getAll()
   