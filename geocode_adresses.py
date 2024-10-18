import requests
import json
import time

import polars as pl
from tqdm import tqdm



base_url = "https://nominatim.openstreetmap.org/search?format=json&polygon=0&addressdetails=1&q="
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"

headers = {
    'User-Agent': user_agent,
    'Referer' : 'tobias.schulzeheinrichs@gmail.com'
}



addresses = []
with open("addresses.csv", "r") as f:
    addresses = f.readlines()

geo_coords = []
for ad in tqdm(addresses):
    if ad is None or len(ad) == 0:
        continue
    (name, address) =  ad.split(";")
    encoded_addres = address.replace(" ", "+")
    resp = requests.get(f"{base_url}{encoded_addres}+21035+hamburg+germany", headers = headers)
    json_string = resp.content.decode("utf-8")
    json_resp = json.loads(json_string)
    if len(json_resp) == 0:
        print(f"Failed to geocode {name}")
        break
    geo_coords.append({"name" : name, "lat" : json_resp[0]["lat"], "lon": json_resp[0]["lon"]})
    time.sleep(1)


dfa = pl.from_dicts(geo_coords, schema={"name" : pl.Utf8, "lat": pl.Float64, "lon": pl.Float64})
print(dfa)
dfa.write_csv("geo_coords.csv")
