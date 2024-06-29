from dao.connection import DataBase
import json
import pathlib
import PIL.Image
import google.generativeai as genai
import google.ai.generativelanguage as glm
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from dotenv import load_dotenv
import base64
from PIL import Image
from io import BytesIO

from dao.model import Ingredeint, Product
load_dotenv()
class ApexService:
    def __init__(self):
        self.db = DataBase().db
        self.apex_collection = self.db['products']
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    def getAll(self):
        data = self.apex_collection.find({})  
        res = []
        for val in data:
            val["_id"]= str(val["_id"])
            res.append(val)
        
        return res
    def apexAdd(self,name,img):
        model1=genai.GenerativeModel("gemini-pro-vision")
        model2=genai.GenerativeModel(model_name="gemini-pro", generation_config={
          "temperature": 0.3  # Set the temperature to 0.3
          # "top_p": 1,
          # "top_k": 32,
          # "max_output_tokens": 2048
         })
        prompt_template4 = """
            "input": "{input_placeholder}",
            "information": "the input contains a comma seperated string containing names of different ingredients"
            "context": "You are an advanced AI trained to evaluate the ingredients provided",
            "task": "Analyze all the ingredients provided in the input for allergic content",
            "instruction": "Identify the allergies caused by each ingredients if any and give detailed explaination of the symptoms caused by these allergies",
            "instruction": "follow the below output format and the output should be in a valid json format",
            "output-format": "
              [
                  "ingredient": [the value here should be the name of the ingredient],
                  "allergy": [the value here should be comma separated name of all allergies cause by this ingredient],
                  "description": [the value here should be a description about the identified allergies]
              ]",
             "example-response":
 
              [
                  [
                      "ingredient": "Sugar",
                      "allergy": "No",
                      "description": "True sugar allergies are extremely rare. It's more likely to be a sugar intolerance than an allergy."
                  ],
       
                  [
                      "ingredient": "Palm Oil",
                      "allergy": "Yes",
                      "description": "Palm oil is a common allergen. It can cause a range of symptoms, including skin rashes, hives, swelling, and difficulty breathing. In some cases, it can even be fatal."
                  ],
       
                  [
                      "ingredient": "Seasoning",
                      "allergy": "Yes",
                      "description": "The seasoning on this product contains a number of ingredients that can cause allergies, including milk, soy, and wheat."
                  ]
                        ] 
          """
        
        image_template = "Give all the ingredients mentioned in this image in comma separated string format"
        decoded_image = base64.b64decode(img)
        image_buffer = BytesIO(decoded_image)
        image = Image.open(image_buffer)
        response1=model1.generate_content(
            [image_template, image],
            stream=True,
            safety_settings={
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
            }
        )
   
        response1.resolve()
        text= str(response1.text)

        response2=model2.generate_content(
            prompt_template4.format(input_placeholder= text),
            stream=True,
            safety_settings={
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
            }
        )
        response2.resolve() 
        res=response2.text
        res= json.loads(res)
        print(type(res))
        ingredients = [Ingredeint(**item) for item in res]
        product = Product(product=name, report=ingredients)
        self.apex_collection.insert_one(product.model_dump())
        return res

        
