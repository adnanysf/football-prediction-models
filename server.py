from fastapi import FastAPI
from dotenv import load_dotenv
import os
import requests

load_dotenv(".env")
APIFOOTBALL_KEY = os.getenv('APIFOOTBALL_API_KEY', "FALSE")
APIFOOTBALL_URL = os.getenv('APIFOOTBALL_API_URL', "FALSE")
debug_mode = os.getenv('DEBUG', 'False')

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/leagues/{givenCountry}")
async def get_leagues(givenCountry: str):
    if APIFOOTBALL_KEY == "FALSE" or APIFOOTBALL_URL == "FALSE":
        return {"error": "API key or URL not set in environment variables."}
    country = givenCountry
    payload={}
    url = f"{APIFOOTBALL_URL}/leagues?" + "country=" + country
    headers = {
    'x-rapidapi-key': APIFOOTBALL_KEY,
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        returnJSON = []
        res = response.json()
        res = res.get('response', [])
        if res:
            for league in res:
                returnJSON.append({
                    'id': league.get('league', {}).get('id', ''),
                    'name': league.get('league', {}).get('name', ''),
                })
        return returnJSON
    else:
        return {"error": f"Failed to fetch leagues: {response.status_code}"}