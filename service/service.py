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
    def apexAdd(self,name,img, img2):
        model1=genai.GenerativeModel("gemini-pro-vision")

        model2=genai.GenerativeModel(model_name="gemini-pro", generation_config={
          "temperature": 0.3 , # Set the temperature to 0.3
          # "top_p": 1,
          # "top_k": 32,
          "max_output_tokens": 2048
         })
        prompt_template4 = """
            "input": "{input_placeholder}",
            "information": "the input contains a comma seperated string containing names of different ingredients"
            "context": "You are an advanced AI trained to evaluate the ingredients provided",
            "task": "Analyze at max 15 important ingredients provided in the input for allergic content",
            "instruction": "Identify the allergies caused by each ingredients if any and give detailed explaination of the symptoms caused by these allergies",
            "instruction": "follow the below output format and the output should be strictly in a valid json format",
            "instruction": "the output should contain maximum 15 most important ingredients",
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
        text3 = ""
        if img2:
            # image_template = "The provided image is the prescription of a patient describing the allergies and allergens of that patient. I want you to provide me a comma separated string containing those allergies and allergens."
            prompt_template2 = """
            "information": "the input image is a prescription about the patient"
            "context": "You are an advanced AI trained to evaluate the prescription and extract the allergies and allergens of the patient",
            "task": "Analyze the image a provide the allergies and allergens of the patient",
            "output-format": "should be a comma separated string containing all the allergies and allergens"
            """
            decoded_image = base64.b64decode(img2)
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
            text2= str(response1.text)

            prompt_template = """
            "input1": "{input_placeholder1}",
            "input2": "{input_placeholder2}",
            "information": "the input1 contains a comma separated string of ingredients in a product"
            "information": "the input2 contains the information of a patient about his allergies and allergens"
            "context": "You are an advanced AI trained to evaluate if any ingredient from the product is harmfull for the patient or not",
            "task": "Analyze both the inputs and generate a report describing if the product is harmful for the patient or not",
            "information": "If the product is harmfull for the patient then you should describe which ingredient of the product is harmfull for the patient and why"
            "information": "If the product is not harmfull for the patient then you should just explain if the product has some positive effect for the patient"
            "output-format": "The output should be a string containing all the information".
            """
            response3=model2.generate_content(
                prompt_template.format(input_placeholder1 = text, input_placeholder2=text2),
                stream=True,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
                }
            )
            response3.resolve()
            text3= str(response3.text)
    

        text3 = text3.replace("json", "")
        print(text3)

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
        print(res)
        res= json.loads(res)
        res_obj = {
            "ingredients": res,
            "product_name": name,
            "explaination": text3
        }

        ingredients = [Ingredeint(**item) for item in res]
        product = Product(product=name, report=ingredients)
        self.apex_collection.insert_one(product.model_dump())
        return res_obj
