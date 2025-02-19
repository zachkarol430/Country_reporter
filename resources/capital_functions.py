from Chat_bot import generate_fun_facts
from weather_helper import get_weather  # Import the weather function
from extract_flag import get_flag_url  # Import the flag URL function
from typing import List, Dict
import random
from fastapi import HTTPException
from Capital_info_getters import get_capital_info
import os
import pandas as pd
from fastapi import APIRouter

# Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../Data')  # Adjusted to point to the correct Data directory
FLAGS_DIR = os.path.join(DATA_DIR, 'flags')

router = APIRouter()

def load_country_details() -> pd.DataFrame:
    """Load country details from CSV"""
    try:
        # Ensure the file path is correct
        return pd.read_csv(os.path.join(DATA_DIR, 'merged_gdp_country_details.csv'))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV file not found. Please check the file path.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading country details: {str(e)}")

@router.get("/capital/{capital_name}")
async def get_capital_info_endpoint(capital_name: str) -> Dict:
    """Get information about a specific capital"""
    country_details_df = load_country_details()
    
    # Find the row with the specified capital
    capital_row = country_details_df[country_details_df['capital'].str.lower() == capital_name.lower()]
    
    if capital_row.empty:
        raise HTTPException(status_code=404, detail="Capital not found")
    
    # Extract relevant data
    country_data = capital_row.iloc[0]
    
    # Get capital info
    capital_info = get_capital_info(country_data['capital'], country_data['latitude'], country_data['longitude'])
    weather_data = get_weather(country_data['capital']) 
    
    return {
        "capital": capital_info['capital'],
        "weather": {
            "temperature": weather_data['main']['temp'] if weather_data else None,
            "description": weather_data['weather'][0]['description'] if weather_data else None,
            "humidity": weather_data['main']['humidity'] if weather_data else None,
            "wind_speed": weather_data['wind']['speed'] if weather_data else None,
        } if weather_data else None,
        "image_url": capital_info['image_url'],
        "maps_link": capital_info['maps_link'],
        "country_name": country_data['country_name'],
        "government_type": country_data['government_type'],
        "currency": country_data['currency'],
    }