import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def get_country_names():
    try:
        with open('Data/Country_site_names.txt', 'r') as file:
            content = file.read()
            
        country_names = set()
        urls = content.split()
        
        for url in urls:
            if '/country/' in url and '/population' in url:
                # Extract country name between /country/ and /population
                country = url.split('/country/')[1].split('/population')[0]
                country_names.add(country)
                
        return sorted(list(country_names))
    except Exception as e:
        print(f"Error reading country names file: {str(e)}")
        return []

def standardize_country_name(name):
    # Remove spaces and special characters
    name = name.replace(' ', '')
    name = name.replace('.', '')
    name = name.replace(',', '')
    name = name.replace('-', '')
    return name

def map_country_name(country):
    try:
        with open('Data/Mappings.txt', 'r', encoding='utf-8') as file:
            mappings = file.readlines()
            
        for mapping in mappings:
            mapping = mapping.strip()
            if not mapping:  # Skip empty lines
                continue
                
            try:
                old_name, new_name = mapping.split(' : ')
                if old_name == country:
                    print(f"Mapping {country} to {new_name}")
                    return new_name
            except ValueError:
                print(f"Invalid mapping format: {mapping}")
                continue
                
        return country
        
    except FileNotFoundError:
        print("Mappings.txt file not found")
        return country
    except Exception as e:
        print(f"Error reading mappings file: {str(e)}")
        return country

def get_country_data(country):
    try:
        # Standardize country name for URL
        country_url = standardize_country_name(country)
        url = f"http://countryreports.org/country/{country_url}.htm"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the facts section
        facts_section = soup.find('div', class_='crpBodyOut')
        
        # Extract data from the table
        table = facts_section.find('table', class_='crpSectionTable')
        rows = table.find_all('tr')
        
        country_data = {
            "country_name": country
        }
        
        # Map field names to table row headers
        field_map = {
            "Capital": "capital",
            "Government Type": "government_type",
            "Currency": "currency", 
            "Language": "language",
            "Total Area": "total_area",
            "Location": "location",
            "GDP - real growth rate": "gdp_growth",
            "GDP - per capita (PPP)": "gdp_per_capita"
        }
        
        # Extract data from each row
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                header = cells[0].text.strip()
                value = cells[1].text.strip()
                
                if header in field_map:
                    # Remove any note lines that appear after newlines
                    value = value.split('\n')[0].strip()
                    country_data[field_map[header]] = value
                    
        return country_data
            
    except Exception as e:
        import traceback
        print(f"Error fetching data for {country}:")
        print(traceback.format_exc())
        
        # Append failed country to errors file
        error_file = 'Data/failed_countries.txt'
        os.makedirs('Data', exist_ok=True)
        with open(error_file, 'a') as f:
            f.write(f"{country}\n")
            
        return None

def main():
    # Get list of countries from your existing GDP or Population CSV
    df = pd.read_csv('Data/GDP.csv')
    
    # Get standardized country names from country_names.txt
    standard_country_names = get_country_names()
    
    # Create a mapping dictionary for country name standardization
    country_name_map = {}
    for std_name in standard_country_names:
        # Create variations of the name for matching
        variations = [
            std_name,
            std_name.lower(),
            std_name.replace('-', ' '),
            std_name.replace('_', ' ')
        ]
        for var in variations:
            country_name_map[var] = std_name
    
    # Standardize country names in the DataFrame
    df['Country Name'] = df['Country Name'].apply(standardize_country_name)
    
    # Map country names using the mapping file
    df['Country Name'] = df['Country Name'].apply(map_country_name)
    
    countries = df['Country Name'].tolist()
    
    # List to store country data
    all_country_data = []
    
    # Iterate through countries
    for country in countries:
        print(f"Fetching data for {country}...")
        country_data = get_country_data(country)
        
        if country_data:
            all_country_data.append(country_data)
        
        # Add delay to be respectful to the server
        time.sleep(2)
    
    # Convert to DataFrame
    df_countries = pd.DataFrame(all_country_data)
    
    # Create output directory if it doesn't exist
    os.makedirs('Data', exist_ok=True)
    
    # Save to CSV
    output_path = 'Data/country_details.csv'
    df_countries.to_csv(output_path, index=False)
    print(f"\nData saved to {output_path}")

if __name__ == "__main__":
    main()
