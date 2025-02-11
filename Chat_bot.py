from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import random
import os
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

# Create flags directory if it doesn't exist
os.makedirs('flags', exist_ok=True)

# Download all country flags first
def download_all_flags(country_data):
    for key in country_data:
        df = country_data[key]
        for country in df['Country Name'].unique():
            # Use the same standardization function for flag filenames
            flag_filename = f"flags/{standardize_country_name(country)}_flag.png"
            
            # Skip if flag already exists
            if os.path.exists(flag_filename):
                continue
                
            try:
                country_response = requests.get(f'https://restcountries.com/v3.1/name/{country}')
                country_info = country_response.json()
                flag_url = country_info[0]['flags']['png']
                
                response = requests.get(flag_url)
                flag_image = Image.open(BytesIO(response.content))
                flag_image.save(flag_filename)
                print(f"Downloaded flag for {country}")
                
            except Exception as e:
                print(f"Could not download flag for {country}: {str(e)}")

model = OllamaLLM(model="llama3.2:1b")

folder_path = 'Data'
country_details_df = pd.read_csv('Data/country_details.csv')

# Choose a random country index
country_index = random.randint(0, len(country_details_df) - 1)

# Get country name and details
country = country_details_df.iloc[country_index]['country_name']
capital = country_details_df.iloc[country_index]['capital']
gov_type = country_details_df.iloc[country_index]['government_type']
currency = country_details_df.iloc[country_index]['currency']

prompt = f"""
Generate a report for {country} with the following information:
- **Capital**: {capital}
- **Government Type**: {gov_type}
- **Currency**: {currency}

Additionally, generate the following dynamically:
- ** Give me two fun facts about {country}. **
- DO NOT ADD ANYTHING ELSE TO THE REPORT.
"""

#reprompt if about terriosm lol dont talk about terrorism


# Create a chat prompt template
prompt_template = ChatPromptTemplate.from_template(prompt)

# Initialize response variable
response = None

def standardize_country_name(country):
    """Convert country name to standard format for filenames"""
    # Replace spaces and hyphens with underscores
    standardized = country.replace(' ', '_').replace('-', '_')
    # Handle special cases like BurkinaFaso -> burkina_faso
    standardized = '_'.join(
        ''.join(c.lower() if not c.isupper() or i == 0 
                else f'_{c.lower()}' for i, c in enumerate(word))
        for word in standardized.split('_')
    )
    return standardized

try:
    # Set a timeout and add error handling for the model invocation
    response = model.invoke(
        prompt,
        config={
            'timeout': 30,  # 30 second timeout
            'max_tokens': 500  # Limit response length
        }
    )
    
    # Use standardized country name for flag filename
    flag_filename = f"flags/{standardize_country_name(country)}_flag.png"
    if not os.path.exists(flag_filename):
        print(f"\nFlag file not found for {country}")
    
except Exception as e:
    print(f"Error generating report: {str(e)}")
finally:
    # Generate PDF report only if we have a response
    if response:
        try:
            # Create reports directory on desktop if it doesn't exist
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'country_reports')
            os.makedirs(desktop_path, exist_ok=True)

            # Create PDF
            pdf_filename = os.path.join(desktop_path, f"{country.lower().replace(' ', '_')}_report.pdf")
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from reportlab.lib.utils import ImageReader

            c = canvas.Canvas(pdf_filename, pagesize=letter)
            
            # Add title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, f"Country Report: {country}")
            
            # Add report content
            c.setFont("Helvetica", 12)
            y_position = 700
            # Split the response string directly since it's not an object
            for line in str(response).split('\n'):
                if line.strip():
                    c.drawString(50, y_position, line)
                    y_position -= 20
                    
            # Add flag if available
            if os.path.exists(flag_filename):
                flag = ImageReader(flag_filename)
                c.drawImage(flag, 50, y_position - 150, width=200, height=120)
                
            c.save()
            print(f"\nPDF report generated: {pdf_filename}")
            
        except Exception as e:
            print(f"Error generating PDF report: {str(e)}")
    else:
        print("No response available to generate PDF report")

