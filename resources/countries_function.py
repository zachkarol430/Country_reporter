from Chat_bot import generate_fun_facts,summarize_news
from weather_helper import get_weather  # Import the weather function
from extract_flag import get_flag_url  # Import the flag URL function
import pandas as pd
import os
from fastapi import HTTPException
from typing import List, Dict
import random
from fastapi.responses import FileResponse
from Capital_info_getters import get_capital_info
from fastapi import APIRouter
from News_collector import fetch_google_news_rss


# Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../Data')  # Adjusted to point to the correct Data directory
FLAGS_DIR = os.path.join(DATA_DIR, 'flags')

router = APIRouter()

# Data loading functions
def load_gdp_data() -> pd.DataFrame:
    """Load GDP data from CSV"""
    try:
        return pd.read_csv(os.path.join(DATA_DIR, 'GDP.csv'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading GDP data: {str(e)}")

def load_country_details() -> pd.DataFrame:
    """Load country details from CSV"""
    try:
        return pd.read_csv(os.path.join(DATA_DIR, 'merged_gdp_country_details.csv'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading country details: {str(e)}")


@router.get("/countries")
async def get_countries() -> List[str]:
    """Get list of all countries"""
    df = load_gdp_data()
    return df['Country Name'].unique().tolist()


@router.get("/search/{query}")
async def search_countries(query: str):
    """Search for countries by name"""
    df = load_gdp_data()
    matches = df[df['Country Name'].str.contains(query, case=False, na=False)]
    return {
        "matches": matches['Country Name'].unique().tolist(),
        "total_matches": len(matches['Country Name'].unique())
    }

@router.get("/random-country")
async def get_random_country() -> Dict:
    """Get information about a random country"""
    country_details_df = load_country_details()
    
    # Choose a random country index
    country_index = random.randint(0, len(country_details_df) - 1)
    
    # Get country details
    country_data = country_details_df.iloc[country_index]
    
    # Generate fun facts
    fun_facts = generate_fun_facts(country_data['country_name'])
    
    # Fetch weather data for the capital
    weather_data = get_weather(country_data['capital'])  # No need to pass the API key
    
    # Get the flag URL using the ISO code
    flag_url = get_flag_url(country_data['Country Code'])  # Assuming 'Country Code' is the column for country codes
    
    # Get capital info
    capital_info = get_capital_info(country_data['capital'], country_data['latitude'], country_data['longitude'])

    # Fetch news data
    news_data = fetch_google_news_rss(country_data['country_name'])
    news_summary = summarize_news(news_data,country_data['country_name'])
    
    return {
        "country_name": country_data['country_name'],
        "flag_url": flag_url,
        "capital": capital_info['capital'],
        "image_url": capital_info['image_url'],
        "maps_link": capital_info['maps_link'],
        "government_type": country_data['government_type'],
        "currency": country_data['currency'],
        "fun_facts": fun_facts,
        "weather": {
            "temperature": weather_data['main']['temp'] if weather_data else None,
            "description": weather_data['weather'][0]['description'] if weather_data else None,
            "humidity": weather_data['main']['humidity'] if weather_data else None,
            "wind_speed": weather_data['wind']['speed'] if weather_data else None,
        } if weather_data else None, # Include news data in the response
        "news_summary": news_summary    
    }


@router.get("/flag/{country_name}")
async def get_flag(country_name: str):
    """Get the flag image for the specified country"""
    flag_filename = f"{country_name.lower().replace(' ', '_')}_flag.png"
    flag_path = os.path.join(FLAGS_DIR, flag_filename)
    if not os.path.isfile(flag_path):
        raise HTTPException(status_code=404, detail="Flag image not found")
    return FileResponse(flag_path)
