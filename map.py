import json
import folium

"""
This code creates a visual of where the points of sale are on the map. 
The output is an HTML file.
"""

with open("pointsOfSale_transformed.json", "r", encoding="utf-8") as f:
    points = json.load(f)

m = folium.Map(location=[points[0]["lat"], points[0]["lon"]], zoom_start=10)

for p in points:
    folium.Marker(
        location=[p["lat"], p["lon"]],
        popup=f'{p["name"]} ({p["type"]})'
    ).add_to(m)

m.save("mapa_points_of_sale.html")
