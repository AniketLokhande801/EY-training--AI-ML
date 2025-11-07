from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/solution")
async def extract_field(request: Request):
    try:
        # Parse JSON body
        data = await request.json()

        # Extract the field (change 'name' to any field you want)
        name = data.get("query")

        if name is None:
            return JSONResponse(
                status_code=400,
                content={"error": "Field 'name' not found in request."}
            )

        # Return the extracted field
        return {"extracted_name": name}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
