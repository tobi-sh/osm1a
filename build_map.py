import folium
import pandas as pd

def build_map(add):
    center = calc_center(add)
    m = folium.Map(location=center, zoom_start=15)


    for name in add.to_dict(orient="records"):
        folium.Marker(
            location=[name["Lat"], name["Lon"]],
            popup=name["Name"],
        ).add_to(m)


    m.save("osm_1a.html")


def read_coords():
    addresses = pd.read_csv("geo_coords.csv", sep=",")
    print(addresses.head())
    return addresses

def calc_center(add):
    return [add["Lat"].mean(), add["Lon"].mean()]


if __name__ == '__main__':
    build_map(read_coords())


