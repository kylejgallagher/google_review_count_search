import serpapi as sp
import pandas as pd
from serpapi import GoogleSearch

key = ""

search_location = "Shibuya"
search_term = "Ramen"

params = {
    "engine": "google_maps",
    "q": f"{search_term} {search_location}",
    "hl": "ja",
    "gl": "jp",
    "type":"search",
    "api_key": key
}

search = GoogleSearch(params)
results = search.get_dict()

print(results)

# FIX: extract array directly
ramen_data = results.get("local_results", [])
df_ramen = pd.json_normalize(ramen_data)



# df_ramen = df_ramen.rename(columns={
#     'gps_coordinates.latitude': 'latitude',
#     'gps_coordinates.longitude': 'longitude',
#     'service_options.dine_in': 'dine_in',
#     'service_options.takeout': 'takeout',
#     'service_options.no_delivery': 'no_delivery'
# })

df_ramen_final = df_ramen[['title','rating','reviews','reviews_link','address','website']]

print(df_ramen.columns.tolist())
print(df_ramen_final)
