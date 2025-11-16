import pandas as pd
from serpapi import GoogleSearch
from geopy.geocoders import Nominatim
import time

# insert SerpAPI key
key = ""
MAX_PAGES = 11

def location_to_coord(location_name,zoom=13):
    geolocator = Nominatim(user_agent='"my_ramen_app/1.0 (kylejgallagher@yahoo.com)"')
    location = geolocator.geocode(location_name)

    if location:
        lat = location.latitude
        lng = location.longitude
        return f'@{lat},{lng},{zoom}z'
input_location = input("Enter a location: ")
location_data = location_to_coord(input_location)
input_search_item = input("What do you want to search? ")
q = input_search_item

print(location_data)
#
params = {
  "engine": "google_maps",
  "q": q,
  "ll": location_data,
  "type": "search",
  "hl": "ja",
  "gl": "jp", 
  "api_key": key
}

# 2. --- Fetch Results and Paginate ---
search = GoogleSearch(params)
all_cafe_data = []
page_counter = 0

# The pagination() method returns a generator that fetches subsequent pages
# automatically by updating the 'start' parameter.
for results in search.pagination():
    page_counter += 1

    # Extract the local_results from the current page's response
    local_results = results.get('local_results')

    if local_results:
        print(f"Collected {len(local_results)} results from page {page_counter}...")
        all_cafe_data.extend(local_results)
    else:
        print(f"No local results found on page {page_counter}. Stopping.")
        break

    # Stop after collecting the specified number of pages
    if page_counter >= MAX_PAGES:
        print(f"Reached maximum page limit of {MAX_PAGES}. Stopping pagination.")
        break

# 3. --- Process and Flatten Data into DataFrame ---
if all_cafe_data:
    # pd.json_normalize flattens nested dictionaries (like coordinates)
    df_results = pd.json_normalize(all_cafe_data)

    # Define the final columns we want and their clean names
    final_columns = {
        'title': 'Place Name',
        'gps_coordinates.latitude': 'Latitude',
        'gps_coordinates.longitude': 'Longitude',
        'rating': 'Rating',
        'reviews': 'Review Count'
    }

    # Filter and rename the columns in the final DataFrame
    df_final = df_results[[c for c in final_columns.keys() if c in df_results.columns]].rename(columns=final_columns)
    df_final = df_final[df_final["Review Count"] > 500]

    print(f"\n--- Consolidated {input_search_item} Data ---")
    print(f"Total Spots Retrieved: {len(df_cafes)}")
    print(f"Total Good Spots Retrieved: {len(df_final)}")
    print(df_final.head())
    df_final.to_csv(f"{input_search_item}_{input_location}.csv")
else:
    print("Failed to retrieve any data.")
