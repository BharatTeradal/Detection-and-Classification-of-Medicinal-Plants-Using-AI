from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from inference_sdk import InferenceHTTPClient
from typing import List, Optional
import shutil
import os
import csv
import json
import requests
from datetime import datetime
from collections import Counter

app = FastAPI()
from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles
# app.mount("/Crop-Recommendation-System-Using-Machine-Learning-main", StaticFiles(directory="Crop-Recommendation-System-Using-Machine-Learning-main"), name="crop_system")


templates = Jinja2Templates(directory="templates")
import pickle

model = pickle.load(open("plant_recommendation/model.pkl", "rb"))
sc = pickle.load(open("plant_recommendation/standscaler.pkl", "rb"))
ms = pickle.load(open("plant_recommendation/minmaxscaler.pkl", "rb"))

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Roboflow client
client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="vbVqpG5KXNHpVL7AA0Iu"
    
)

# Serve frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

from fastapi import Form
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from PIL import Image
import io
from fastapi.staticfiles import StaticFiles

app = FastAPI()
from fastapi import Request
from fastapi.responses import HTMLResponse
# ...existing code...

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# app = FastAPI()

# # Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Set up templates (adjust path as needed)
# templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# async def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
# # ...existing code...
# templates = Jinja2Templates(directory="plant_recommendation")
# @app.get("/", response_class=HTMLResponse)
# async def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
# @app.get("/recommendation", response_class=HTMLResponse)
# async def read_index(request: Request):
#     return templates.TemplateResponse("/templates/index.html", {"request": request})


# @app.get("/recommendation")
# async def dashboard(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})
# @app.post("/predict_crop", response_class=HTMLResponse)
# async def predict_crop(
#     request: Request,
#     Nitrogen: float = Form(...),
#     Phosporus: float = Form(...),
#     Potassium: float = Form(...),
#     Temperature: float = Form(...),
#     Humidity: float = Form(...),
#     Ph: float = Form(...),
#     Rainfall: float = Form(...)
# ):
#     try:
#         features = np.array([[Nitrogen, Phosporus, Potassium, Temperature, Humidity, Ph, Rainfall]])
#         scaled = ms.transform(features)
#         final_input = sc.transform(scaled)
#         prediction = model.predict(final_input)

#         crop = crop_dict.get(prediction[0], "Unknown")
#         result = f"{crop} is the best crop to be cultivated right there" if crop != "Unknown" else "Could not determine the best crop."

#         return templates.TemplateResponse("index.html", {"request": request, "result": result})
#     except Exception as e:
#         return templates.TemplateResponse("index.html", {"request": request, "result": f"Error: {str(e)}"})


# Crop dictionary
crop_dict = {
    1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
    8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
    14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
    19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
}

# ...existing imports...
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates (adjust path as needed)
templates = Jinja2Templates(directory="plant_recommendation/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/recommendation", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict_crop", response_class=HTMLResponse)
async def predict_crop(
    request: Request,
    Nitrogen: float = Form(...),
    Phosporus: float = Form(...),
    Potassium: float = Form(...),
    Temperature: float = Form(...),
    Humidity: float = Form(...),
    Ph: float = Form(...),
    Rainfall: float = Form(...)
):
    try:
        features = np.array([[Nitrogen, Phosporus, Potassium, Temperature, Humidity, Ph, Rainfall]])
        scaled = ms.transform(features)
        final_input = sc.transform(scaled)
        prediction = model.predict(final_input)

        crop = crop_dict.get(prediction[0], "Unknown")
        result = f"{crop} is the best crop to be cultivated right there" if crop != "Unknown" else "Could not determine the best crop."

        return templates.TemplateResponse("index.html", {"request": request, "result": result})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "result": f"Error: {str(e)}"})
# ...rest of your code...

# Uploads folder
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load medicinal descriptions (basic info)
def load_basic_descriptions(csv_file_path):
    descriptions = {}
    with open(csv_file_path, newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row["plant_key"].strip().lower()
            descriptions[key] = {
                "name": row["Name"],
                "definition": row["Definition"],
                "applications": row["Applications"],
                "advantages": row["Advantages"],
                "usage": row["Usage"],
                "precautions": row["Precautions"],
                "visit_url": row["Visit_url"]
            }
    return descriptions

# Load healthcare-specific data
def load_healthcare_data(csv_file_path):
    healthcare_info = {}
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row["Plant Name"].strip().lower()
            healthcare_info[key] = {
                "definition": row["Definition"],
                "health_benefits": row["Health Benefits"],
                "traditional_use": row["Traditional Use"],
                "active_compounds": row["Active Compounds"],
                "dosage": row["Dosage"],
                "precautions": row["Precautions"],
                "sources": row["Sources"]
            }
    return healthcare_info

# Load both sets of data at startup
medicinal_descriptions = load_basic_descriptions("medicinal_plants.csv")
healthcare_descriptions = load_healthcare_data("medicinal_plants_healthcare.csv")

# Analytics and report storage
usage_stats = {
    "most_identified_plants": Counter(),
    "region_identifications": Counter(),
    "misclassified_plants": Counter(),
    "monthly_identifications": Counter(),
    "top_species_families": Counter(),
}

# Detailed leaf analysis storage
leaf_analysis_data = {}

def analyze_leaf_image(image_path):
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        return None
        
    # Convert to RGB for better color analysis
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Get image dimensions
    height, width = img.shape[:2]
    
    # Calculate area
    area = height * width
    
    # Color analysis
    avg_color_per_row = np.average(rgb_img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    
    # Get dominant color in HSV
    avg_hsv = cv2.mean(hsv_img)[:3]
    
    # Edge detection for shape analysis
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Shape analysis
    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        perimeter = cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, 0.02 * perimeter, True)
        
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(largest_contour)
        aspect_ratio = float(w)/h
        
        # Calculate leaf metrics
        leaf_area = cv2.contourArea(largest_contour)
        leaf_perimeter = cv2.arcLength(largest_contour, True)
    else:
        aspect_ratio = 0
        leaf_area = 0
        leaf_perimeter = 0
    
    # Determine color name
    def get_color_name(hsv):
        h, s, v = hsv
        if s < 30:
            return "Grey" if v < 128 else "White"
        h = h * 2  # Convert to 0-360 range
        if h < 30 or h > 330:
            return "Red"
        elif 30 <= h < 90:
            return "Yellow-Green"
        elif 90 <= h < 150:
            return "Green"
        elif 150 <= h < 210:
            return "Cyan"
        elif 210 <= h < 270:
            return "Blue"
        elif 270 <= h < 330:
            return "Magenta"
    
    # Texture analysis
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    glcm = np.zeros((256,256))
    h, w = gray.shape
    for i in range(h-1):
        for j in range(w-1):
            glcm[gray[i,j], gray[i,j+1]] += 1
    glcm = glcm / glcm.sum()
    contrast = np.sum(np.square(np.arange(256)[:,None] - np.arange(256)[None,:]) * glcm)
    
    return {
        "dimensions": {
            "width": width,
            "height": height,
            "aspect_ratio": round(aspect_ratio, 2)
        },
        "color": {
            "dominant_color": get_color_name(avg_hsv),
            "rgb": {
                "r": int(avg_color[0]),
                "g": int(avg_color[1]),
                "b": int(avg_color[2])
            },
            "intensity": round(np.mean(gray), 2)
        },
        "shape": {
            "area": round(leaf_area, 2),
            "perimeter": round(leaf_perimeter, 2),
            "circularity": round(4 * np.pi * leaf_area / (leaf_perimeter * leaf_perimeter), 2) if leaf_perimeter > 0 else 0
        },
        "texture": {
            "contrast": round(contrast, 2),
            "smoothness": round(1 - (1 / (1 + contrast)), 2)
        }
    }

@app.post("/analyze_leaf")
async def analyze_leaf(file: UploadFile = File(...)):
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Perform leaf analysis
        analysis_result = analyze_leaf_image(file_path)
        if analysis_result is None:
            return JSONResponse(status_code=400, content={"error": "Could not analyze image"})
        
        # Store analysis result
        leaf_analysis_data[file.filename] = {
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis_result
        }
        
        return JSONResponse(content={
            "filename": file.filename,
            "analysis": analysis_result
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

# Use ipinfo.io to get country from IP
def get_country_from_ip(ip: str) -> Optional[str]:
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            return data.get("country")
    except Exception as e:
        print(f"Error fetching IP info: {e}")
    return None

# Track usage and classification trends
def track_usage_stats(plant_name: str, user_ip: str, timestamp: datetime, species_family: str):
    # Track most identified plants
    usage_stats["most_identified_plants"][plant_name] += 1

    # Region-wise classification
    country = get_country_from_ip(user_ip)
    if country:
        usage_stats["region_identifications"][(plant_name, country)] += 1

    # Monthly stats
    month = timestamp.strftime('%Y-%m')
    usage_stats["monthly_identifications"][(plant_name, month)] += 1

    # Top Species or Families Identified
    usage_stats["top_species_families"][species_family] += 1

@app.post("/predict")
async def predict(files: List[UploadFile] = File(...), user_ip: Optional[str] = None):
    results = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            response = client.infer(file_path, model_id="my-first-project-aeb5w/1")
            predictions = response.get("predictions", {})

            if predictions:
                best_plant = max(predictions.items(), key=lambda item: item[1]['confidence'])
                plant_name = best_plant[0]
                confidence = best_plant[1]['confidence']
                class_id = best_plant[1]['class_id']
                species_family = best_plant[1].get('species_family', 'Unknown')

                key = plant_name.lower()

                # Collect detailed information
                basic_info = medicinal_descriptions.get(key)
                healthcare_info = healthcare_descriptions.get(key)

                # Add extra attributes like size, color, and type
                leaf_type = best_plant[1].get('type', 'Unknown')
                leaf_size = best_plant[1].get('size', 'Unknown')
                leaf_color = best_plant[1].get('color', 'Unknown')

                # Store detailed analysis
                leaf_analysis_data[plant_name] = {
                    "leaf_type": leaf_type,
                    "leaf_size": leaf_size,
                    "leaf_color": leaf_color,
                    "confidence": confidence,
                    "species_family": species_family,
                    "basic_info": basic_info,
                    "healthcare_info": healthcare_info
                }

                # Track usage statistics
                if user_ip:
                    track_usage_stats(plant_name, user_ip, datetime.now(), species_family)

                best_prediction = {
                    "plant_name": plant_name,
                    "confidence": confidence,
                    "class_id": class_id,
                    "leaf_type": leaf_type,
                    "leaf_size": leaf_size,
                    "leaf_color": leaf_color,
                    "basic_info": basic_info,
                    "healthcare_info": healthcare_info
                }
            else:
                best_prediction = {}

            results.append({
                "filename": file.filename,
                "prediction": best_prediction
            })

        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })

        os.remove(file_path)

    return JSONResponse(content=results)

@app.post("/report_accuracy_feedback")
async def report_accuracy_feedback(plant_name: str, user_feedback: str, suggested_correct_name: Optional[str] = None):
    # Track feedback for accuracy improvement
    feedback = {
        "plant_name": plant_name,
        "user_feedback": user_feedback,
        "suggested_correct_name": suggested_correct_name,
        "timestamp": datetime.now().isoformat()
    }

    # Store feedback
    with open("accuracy_feedback.json", "a") as f:
        json.dump(feedback, f)
        f.write("\n")

    return JSONResponse(content={"message": "Accuracy feedback reported successfully"})

# update this  below code as per above provide html to send the data report data also correctly

@app.get("/admin/usage_stats")
async def get_usage_stats():
    return JSONResponse(content=usage_stats)

@app.get("/admin/leaf_analysis")
async def get_leaf_analysis():
    return JSONResponse(content=leaf_analysis_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)