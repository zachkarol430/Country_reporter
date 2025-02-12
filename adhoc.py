#join the two dataframes on the country name column
import pandas as pd

# Load the GDP data
gdp_df = pd.read_csv('Data/GDP.csv')


# Load the population data
country_details_df = pd.read_csv('Data/country_details.csv')

# Merge the dataframes on the country name column, 

merged_df = pd.merge(
    gdp_df,
    country_details_df,
    left_on='Country Name',
    right_on='original_country_name',
    how='inner'
)

# Optional: Print merge diagnostics
print(f"GDP rows: {len(gdp_df)}")
print(f"Country details rows: {len(country_details_df)}")
print(f"Merged rows: {len(merged_df)}")

# Print unmatched countries from GDP data
unmatched_gdp = set(gdp_df['Country Name']) - set(country_details_df['original_country_name'])
if unmatched_gdp:
    print("\nUnmatched countries from GDP data:")
    print(sorted(unmatched_gdp))