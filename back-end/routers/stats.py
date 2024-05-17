from fastapi import APIRouter, HTTPException, Request
from typing import List
import requests

router = APIRouter()

API_KEY = "RGAPI-f9733a73-18e3-4327-aa6e-09d7a15e224e"


@router.get("/user/{user_id}")
async def stats(user_id: str):
    num_games: int = 100

    response = requests.get(
        f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user_id}?api_key={API_KEY}"
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    puuid: str = response.json()["puuid"]

    response = requests.get(
        f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=normal&start=0&count={num_games}&api_key={API_KEY}"
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    games = response.json()

    kills, deaths, assists = 0, 0, 0
    for game in games:
        response = requests.get(
            f"https://americas.api.riotgames.com/lol/match/v5/matches/{game}?api_key={API_KEY}"
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=response.json()
            )
        match_data = response.json()

        for participant in match_data["info"]["participants"]:
            if participant["puuid"] == puuid:
                user_match_data = participant
                break

        kills += user_match_data["kills"]
        deaths += user_match_data["deaths"]
        assists += user_match_data["assists"]

    return {
        user_id: {
            "kills": kills / num_games,
            "deaths": deaths / num_games,
            "assists": assists / num_games,
        }
    }
