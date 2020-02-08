import folium
import pandas as pd


mapa = folium.Map(location=[-15.788497,-47.879873],zoom_start=4)
folium.Marker([-19.9166813,-43.9344931]).add_to(mapa)
mapa