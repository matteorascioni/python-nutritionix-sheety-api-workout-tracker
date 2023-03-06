# Before to run this program this program run this commands:
# python3 -m venv venv
# pip3 install requests
import os
import json
import requests
from datetime import datetime

APP_ID = os.environ["NT_APP_ID"] #Your nutritionix APP_ID
API_KEY = os.environ["NT_API_KEY"] #Your nutritionix API_KEY
BEARER_TOKEN = os.environ['BEARER_TOKEN'] #Your Sheety BEARER_TOKEN

GENDER = "" #Your gender
WEIGHT_KG = 0 #Your weight
HEIGHT_CM = 0 #Your height
AGE = 0 #Your age

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2"
sheety_endpoint = os.environ["SHEETY_ENDPOINT"]

# Nutriotionix API
exercise_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_text = input("Tell me which exercises you did: ")

natural_execrise_data = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}
natural_exercise_endpoint = f"{nutritionix_endpoint}/natural/exercise"
response = requests.post(url=natural_exercise_endpoint, json=natural_execrise_data, headers=exercise_headers)
result = response.json()

# Date and time
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Sheety API
bearer_headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}
for exercise in result["exercises"]:
    # Google sheet columns
    google_sheet_data = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    # Posts the google_sheet_data to the Google Sheet File
    post_google_sheet_data = requests.post(url=sheety_endpoint, json=google_sheet_data, headers=bearer_headers)