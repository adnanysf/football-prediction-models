from fastapi import FastAPI
from dotenv import load_dotenv
import os
import requests
from datetime import timedelta
import requests_cache

load_dotenv(".env")
APIFOOTBALL_KEY = os.getenv('APIFOOTBALL_API_KEY', "FALSE")
APIFOOTBALL_URL = os.getenv('APIFOOTBALL_API_URL', "FALSE")
debug_mode = os.getenv('DEBUG', 'False')

requests_cache.install_cache('football_api_cache', expire_after=timedelta(weeks=1))

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

@app.get("/teams/{leagueId}")
async def get_teams(leagueId: int):
    if APIFOOTBALL_KEY == "FALSE" or APIFOOTBALL_URL == "FALSE":
        return {"error": "API key or URL not set in environment variables."}
    payload={}
    url = f"{APIFOOTBALL_URL}/teams?" + "league=" + str(leagueId) + "&season=2023"
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
            for team in res:
                returnJSON.append({
                    'id': team.get('team', {}).get('id', ''),
                    'name': team.get('team', {}).get('name', ''),
                })
        return returnJSON
    else:
        return {"error": f"Failed to fetch teams: {response.status_code}"}


@app.get("/stats/{teamId}/{leagueId}")
async def get_stats(teamId: int, leagueId: int):
    if APIFOOTBALL_KEY == "FALSE" or APIFOOTBALL_URL == "FALSE":
        return {"error": "API key or URL not set in environment variables."}
    payload={}
    url = f"{APIFOOTBALL_URL}/teams/statistics?" + "team=" + str(teamId) + "&league=" + str(leagueId) + "&season=2023"
    headers = {
    'x-rapidapi-key': APIFOOTBALL_KEY,
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        stats = response.json().get('response', {})
        if not stats:
            return {"error": "No statistics found for the given team and league."}
        goals_stats = stats.get('goals', {})
        if not goals_stats:
            return {"error": "No goals statistics found for the given team and league."}
        response = {
            'team_id': teamId,
            'league_id': leagueId,
            'goals': goals_stats
        }
        return response
    else:
        return {"error": f"Failed to fetch stats: {response.status_code}"}