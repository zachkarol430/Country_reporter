#join the two dataframes on the country name column
import pandas as pd
import json
import requests
# Load the GDP data
gdp_df = pd.read_csv('Data/GDP.csv')









# Load the population data
country_details_df = pd.read_csv('Data/country_details.csv')


#join with myenv/data jsons



# Merge the dataframes on the country name column, 

#only keep 'Country Name' and 'Country Code' columns in gdp
gdp_df = gdp_df[['Country Name', 'Country Code']]

merged_df = pd.merge(
    gdp_df,
    country_details_df,
    left_on='Country Name',
    right_on='original_country_name',
    how='inner'
)

# Initialize lists to store capitals and their lat/lng
capitals = []
latitudes = []
longitudes = []

# Extract capital and capital info
for code in merged_df["Country Code"]:
    url = f"https://restcountries.com/v3.1/alpha/{code}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            # Extract capital and capital info
            capital = data[0]['capital'][0] if 'capital' in data[0] else None
            capital_info = data[0].get('capitalInfo', {})
            latlng = capital_info.get('latlng', [None, None])  # Get lat/lng, default to [None, None]
            
            # Append to lists
            capitals.append(capital)
            latitudes.append(latlng[0])  # Latitude
            longitudes.append(latlng[1])  # Longitude
            
            print(f"Country Code: {code}, Capital: {capital}, Latitude: {latlng[0]}, Longitude: {latlng[1]}")
    else:
        print(f"Error fetching data for country code {code}: {response.status_code}")
        capitals.append(None)
        latitudes.append(None)
        longitudes.append(None)

# Add capitals, latitudes, and longitudes to merged_df
merged_df['capital'] = capitals
merged_df['latitude'] = latitudes
merged_df['longitude'] = longitudes

# Save the merged dataframe to a new CSV file
merged_df.to_csv('Data/merged_gdp_country_details.csv', index=False)





