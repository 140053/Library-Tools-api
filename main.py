from fastapi import FastAPI, Request
import requests
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
app = FastAPI()
from db import Database

TARGET_URL = "http://10.2.42.10:8088/lsystem"


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:4000"],  # Allow requests from Next.js frontend
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.post("/forward")
async def forward_post(request: Request):
    try:
        # Expect only 'idnum' from the client
        data = await request.json()
        idnum = data.get("idnum")

        if not idnum:
            return JSONResponse({"error": "Missing 'idnum' field"}, status_code=400)

        # Preset fields
        library = "LIB-PILI"
        section = "Second Floor"

        # Prepare URL-encoded payload
        payload = f"idnum={idnum}&library={library}&Section={section}"

        # Prepare headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "connect.sid=s%3AgR_HgE31o-rpm3RE60heRQpL5Sq3AXdw.4n9WEwH0UXcKQTzFe%2FV%2FdStLLMTu4AjUY8w6NCaDSV8"
        }

        # Forward the POST request
        response = requests.post(TARGET_URL, headers=headers, data=payload)

        # Return the response from target
        return JSONResponse({
            "status_code": response.status_code,
            "target_response": response.text
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)



@app.get("/books")
async def get_books():
    try:
        conn = Database.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        cursor.close()
        conn.close()

        return JSONResponse(content={"books": jsonable_encoder(books)})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)