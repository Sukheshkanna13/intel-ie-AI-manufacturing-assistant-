from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import os
import shutil
import numpy as np
import joblib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the machine learning models
model_defect = joblib.load('path_to_your_defect_model/model.pkl')  # Replace with actual path for defect model
model_cpu = joblib.load('path_to_your_cpu_model/model.pkl')  # Replace with actual path for CPU model

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered Manufacturing Assistant!"}

@app.post("/upload/defect/")
async def upload_defect_file(file: UploadFile = File(...)):
    try:
        upload_folder = "uploads/"
        os.makedirs(upload_folder, exist_ok=True)  # Ensure the folder exists
        file_location = os.path.join(upload_folder, file.filename)

        # Save the uploaded file to the server
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load the image data for defect analysis (assuming it's an image file)
        image_data = np.load(file_location)  # Modify based on your image handling

        # Run inference using the defect analysis model
        prediction = model_defect.predict(image_data.reshape(1, -1))  # Adjust shape as necessary

        if prediction == 1:  # Assuming 1 means defect found
            return {
                "message": "Defects found! 😢",
                "defect_details": "Crack found on the surface.",
                "file_location": file_location
            }
        else:
            return {
                "message": "Good! No defects found! 😀",
                "file_location": file_location
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {e}")

@app.post("/upload/cpu/")
async def upload_cpu_data(cores: int, freq_mhz: float, tdp_w: float, die_size_mm2: float, transistors_m: float, process_size_nm: float):
    try:
        features = np.array([[cores, freq_mhz, tdp_w, die_size_mm2, transistors_m, process_size_nm]])
        
        # Run inference using the CPU performance model
        cpu_mark_prediction = model_cpu.predict(features)

        return {
            "cpu_mark": float(cpu_mark_prediction[0])  # Ensure output is a float
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CPU data: {e}")

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
            input[type="file"], input[type="text"], input[type="number"] {
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
        <form action="/upload/defect/" enctype="multipart/form-data" method="post">
            <div class="upload-container">
                <input name="file" type="file" required>
                <input type="submit" value="Upload">
            </div>
        </form>
        <h1>CPU Performance Input</h1>
        <form action="/upload/cpu/" method="post">
            <input type="number" name="cores" placeholder="Number of Cores" required>
            <input type="number" name="freq_mhz" placeholder="Frequency (MHz)" required>
            <input type="number" name="tdp_w" placeholder="TDP (W)" required>
            <input type="number" name="die_size_mm2" placeholder="Die Size (mm^2)" required>
            <input type="number" name="transistors_m" placeholder="Transistors (million)" required>
            <input type="number" name="process_size_nm" placeholder="Process Size (nm)" required>
            <input type="submit" value="Get CPU Mark">
        </form>
        <div class="result" id="result"></div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
