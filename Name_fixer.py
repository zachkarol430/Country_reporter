import pandas as pd
import os

def get_country_names_from_site():
    """Extract country names from site URLs"""
    try:
        with open('Data/Country_site_names.txt', 'r', encoding='utf-8') as file:
            content = file.read().strip()
            
        country_names = set()
        # Split content into URLs
        urls = content.split()  # Split on whitespace
        
        for url in urls:
            if '/country/' in url:
                # Extract country name between /country/ and next /
                parts = url.split('/country/')
                if len(parts) > 1:
                    country = parts[1].split('/')[0]
                    if '.htm' in country:
                        country = country.split('.htm')[0]
                    if country:
                        country_names.add(country)
                    
        return sorted(list(country_names))
    except Exception as e:
        print(f"Error reading country names file: {str(e)}")
        return []



def main():
    countries = get_country_names_from_site()
    print(f"\nFound {len(countries)} countries:")
    for country in sorted(countries):
        print(country)

if __name__ == "__main__":
    main()
