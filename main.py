
from fastapi import Depends, FastAPI,  Request, Response
from fastapi.exceptions import RequestValidationError
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from router.router import router
# openapi_url="/api/v1/makeathon/openapi.json",
app = FastAPI( docs_url="/api/v1/makeathon/docs")

"""

    Adding the CORS Middleware which handles the requests from different origins

    allow_origins - A list of origins that should be permitted to make cross-origin requests.
                    using ['*'] to allow any origin
    allow_methods - A list of HTTP methods that should be allowed for cross-origin requests.
                    using ['*'] to allow all standard method
    allow_headers - A list of HTTP request headers that should be supported for cross-origin requests. 
                    using ['*'] to allow all headers
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)






"""
incude the routing details of service
"""
app.include_router(router, prefix='/api/v1', tags=['Infosys Makeathon - Apex'])



if __name__ == "__main__":
    print("************************************main start******************************")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("************************************** main end ***************************************")



