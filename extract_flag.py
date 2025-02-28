import requests

def get_flag_url(country_code: str):
    """Fetch the flag URL for a given country code."""
    url = f"https://restcountries.com/v3.1/alpha/{country_code}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            # Extract the PNG flag URL
            flag_url = data[0]['flags']['png']
            return flag_url
    else:
        print(f"Error fetching data for country code {country_code}: {response.status_code}")
        return None

