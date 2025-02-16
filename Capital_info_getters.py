#read in data from country_details.csv
import pandas as pd

country_details_df = pd.read_csv('Data/country_details.csv')
capitals = country_details_df['capital']

#for each capital, get the population
