from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from concurrent.futures import ThreadPoolExecutor
import db  # Import database module
import model  # Import model processing module
from schema import ImageUploadResponse, ClassificationResultResponse

# Initialize the FastAPI app
app = FastAPI()

# ThreadPoolExecutor for async task handling
executor = ThreadPoolExecutor(max_workers=4)

# Endpoint 1: Upload image and trigger processing
@app.post("/upload-image/", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    # Ensure the uploaded file is an image
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    # Read the file contents
    image_data = await file.read()

    # Generate unique ID for the image and store the image in the DB
    image_id = db.insert_image(image_data)

    # Run the image classification asynchronously
    executor.submit(model.process_image, image_data, image_id)
    
    # Return the ID immediately (do not wait for the model result)
    return {"id": image_id}

# Endpoint 2: Get classification result by ID
@app.get("/get-result/{image_id}", response_model=ClassificationResultResponse)
async def get_result(image_id: str):
    # Retrieve result from the database
    result, image_data = db.get_result(image_id)
    
    if result is None:
        return JSONResponse(content={"status": "Processing"}, status_code=202)
    
    # Return the result and the fact that the image is stored in the DB
    return {"id": image_id, "result": result, "image_stored": True}

# Close database connection when the app shuts down
@app.on_event("shutdown")
def shutdown():
    db.close_connection()
