#places to visit, google maps api location
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

#load access and secret keys
load_dotenv()   

UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
UNSPLASH_SECRET_KEY = os.getenv('UNSPLASH_SECRET_KEY')
google_maps_api_key = os.getenv('google_maps_api_key')

# Load country details
country_details_df = pd.read_csv('Data/merged_gdp_country_details.csv')
capitals = country_details_df['capital']


# Function to create Google Maps link
def create_google_maps_link(latitude: float, longitude: float) -> str:
    """Create a Google Maps link for the given latitude and longitude."""
    return f"https://www.google.com/maps/@{latitude},{longitude},15z"  # 15z is the zoom level

# Function to create a static Google Maps image URL
def create_google_maps_image(latitude: float, longitude: float) -> str:
    """Create a Google Maps static image URL for the given latitude and longitude."""
    return f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom=15&size=600x300&markers=color:red%7Clabel:C%7C{latitude},{longitude}&key={google_maps_api_key}"

# Function to get the first image from Wikipedia
def get_wikipedia_image(capital: str):
    """Fetch the first image from Wikipedia for the given capital."""
    search_url = f"https://en.wikipedia.org/wiki/{capital.replace(' ', '_')}"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the first image in the infobox
        infobox = soup.find('table', class_='infobox')
        if infobox:
            img_tag = infobox.find('img')
            if img_tag:
                # Construct the full image URL
                img_url = 'https:' + img_tag['src']
                return img_url
    return None

# Function to get capital info
def get_capital_info(capital: str, latitude: float, longitude: float):
    """Get capital image and Google Maps link."""
    wikipedia_image_url = get_wikipedia_image(capital)  # Get Wikipedia image
    maps_link = create_google_maps_link(latitude, longitude)
    static_map_image = create_google_maps_image(latitude, longitude)  # Get static map image URL
    return {
        "capital": capital,
        "image_url": wikipedia_image_url,  # Prefer Unsplash image, fallback to Wikipedia
        "maps_link": maps_link,
        "static_map_image": static_map_image  # Include static map image URL
    }




