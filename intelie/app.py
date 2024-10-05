from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import os
import shutil
import numpy as np
import joblib  

app = FastAPI()

model = joblib.load('path_to_your_model/model.pkl')  # Replace with the actual path

@app.get("/")
def read_root():
    return {"message": "Welcome to the Defect Analysis API!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        upload_folder = "uploads/"
        os.makedirs(upload_folder, exist_ok=True)  # Ensure the folder exists
        file_location = os.path.join(upload_folder, file.filename)

        # Save the uploaded file to the server
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load the data (adjust according to your file format, here assuming .npy)
        data = np.load(file_location)  # Change if CSV or another format

        # Run inference using the pre-loaded model
        prediction = model.predict(data)  # Ensure the input data shape matches the model's requirement

        # Simulate defect analysis result based on model prediction
        if prediction == 1:  # Assuming 1 means defect found
            defect_type = "Crack"
            defect_description = "Large crack found on the surface."
            return {
                "message": "Defects found! 😢",
                "defect_type": defect_type,
                "defect_description": defect_description,
                "file_location": file_location
            }
        else:
            return {
                "message": "Good! No defects found! 😀",
                "file_location": file_location
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {e}")

@app.get("/upload-form", response_class=HTMLResponse)
def upload_form():
    html_content = """
    <html>
    <head>
        <title>Upload File</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background-color: #f0f4fa;
            }
            h1 {
                color: #4cafef;
            }
            .upload-container {
                margin: 20px 0;
            }
            input[type="file"] {
                padding: 10px;
                border: 2px dashed #4cafef;
                border-radius: 10px;
                cursor: pointer;
                width: 100%;
            }
            input[type="submit"] {
                padding: 10px;
                background-color: #4cafef;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 10px;
            }
            .result {
                margin-top: 20px;
                font-size: 20px;
                color: #333;
            }
            .emoji {
                font-size: 50px;
            }
        </style>
    </head>
    <body>
        <h1>Upload a File for Defect Analysis</h1>
        <form action="/upload/" enctype="multipart/form-data" method="post">
            <div class="upload-container">
                <input name="file" type="file" required>
                <input type="submit" value="Upload">
            </div>
        </form>
        <div class="result" id="result"></div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
