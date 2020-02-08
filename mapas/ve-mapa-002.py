import pandas as pd
import folium

brasil = folium.Map(
    location=[-16.1237611, -59.9219642],    # Coordenadas retiradas do Google Maps
    zoom_start=40
)
brasil.save('teste.html')