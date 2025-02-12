from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
import pandas as pd
import os
from fastapi.middleware.cors import CORSMiddleware
import random
from Chat_bot import generate_fun_facts

app = FastAPI(
    title="Country Data API",
    description="API for accessing country data",
    version="1.0.0"
)

# Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'Data')
FLAGS_DIR = os.path.join(DATA_DIR, 'flags')

# Mount flags directory
app.mount("/flags", StaticFiles(directory=FLAGS_DIR), name="flags")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        return pd.read_csv(os.path.join(DATA_DIR, 'country_details.csv'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading country details: {str(e)}")

@app.get("/countries")
async def get_countries() -> List[str]:
    """Get list of all countries"""
    df = load_gdp_data()
    return df['Country Name'].unique().tolist()

@app.get("/search/{query}")
async def search_countries(query: str):
    """Search for countries by name"""
    df = load_gdp_data()
    matches = df[df['Country Name'].str.contains(query, case=False, na=False)]
    return {
        "matches": matches['Country Name'].unique().tolist(),
        "total_matches": len(matches['Country Name'].unique())
    }

@app.get("/country/{country_name}")
async def get_country_data(
    country_name: str,
    include_gdp: bool = Query(False, description="Include GDP data in response")
):
    """Get all available data for a specific country"""
    try:
        # Load data
        details_df = load_country_details()
        
        # Get basic data
        details = details_df[details_df['country_name'] == country_name].to_dict('records')
        
        # Initialize response
        response = {
            "country_name": country_name,
            "country_details": details[0] if details else None,
            "flag_url": f"/flags/{country_name.lower().replace(' ', '_')}.png"
        }
        
        # Add GDP data if requested
        if include_gdp:
            gdp_df = load_gdp_data()
            gdp_data = gdp_df[gdp_df['Country Name'] == country_name].to_dict('records')
            if gdp_data:
                gdp_data = gdp_data[0]
                # Replace NaN with None for JSON compatibility
                gdp_data = {k: (None if pd.isna(v) else v) for k, v in gdp_data.items()}
            else:
                gdp_data = None
            response["gdp_data"] = gdp_data
            
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/random-country")
async def get_random_country() -> Dict:
    """Get information about a random country"""
    country_details_df = load_country_details()
    
    # Choose a random country index
    country_index = random.randint(0, len(country_details_df) - 1)
    
    # Get country details
    country_data = country_details_df.iloc[country_index]
    
    # Generate fun facts
    fun_facts = generate_fun_facts(country_data['country_name'])
    
    return {
        "country_name": country_data['country_name'],
        "capital": country_data['capital'],
        "government_type": country_data['government_type'],
        "currency": country_data['currency'],
        "fun_facts": fun_facts
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 