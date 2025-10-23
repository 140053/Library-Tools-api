from fastapi import FastAPI, Request
import requests
from fastapi.responses import JSONResponse

app = FastAPI()

TARGET_URL = "http://10.2.42.10:8088/lsystem"

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
