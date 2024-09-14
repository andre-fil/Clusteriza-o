import numpy as np
from sklearn.cluster import DBSCAN
import folium
from datetime import datetime, timedelta


#Coordenadas Frei Germano:
latitudeCFGC = -4.569038553893695
longitudeCFGC = -44.61631006359516


def gerarPontos(latitude, longitude, start_time, interval_seconds, num_pontos):
    pontos = []
    current_time = start_time
    for _ in range(num_pontos):
        pontos.append((latitude, longitude, current_time))
        current_time += timedelta(seconds=interval_seconds)
    return pontos


latitude = -23.550520  
longitude = -46.633308  
start_time = datetime.now()  
interval_seconds = 60  
num_pontos = 5


gps_pontos = gerarPontos(latitudeCFGC, longitudeCFGC, start_time, interval_seconds, num_pontos)


#latitude = -23.560520  
#longitude = -46.643308
latitudeCFGC2 = -4.57905
longitudeCFGC2 = -44.6163103
start_time = datetime.now()  
interval_seconds = 60  
num_pontos = 10

current_time = start_time

gps_pontos.append((latitudeCFGC2, longitudeCFGC2, current_time))

latitudeCFGC3 = -4.58905
longitudeCFGC3 = -44.6263103
start_time = datetime.now()  
interval_seconds = 60  
num_pontos = 10

current_time = start_time

gps_pontos.append((latitudeCFGC3, longitudeCFGC3, current_time))

#for point in gps_pontos:
    #print(f"Latitude: {point[0]}, Longitude: {point[1]}, Timestamp: {point[2]}")





coordinates = np.array([(point[0], point[1]) for point in gps_pontos])

dbscan = DBSCAN(eps=0.001, min_samples=1) 
labels = dbscan.fit_predict(coordinates)


for i, label in enumerate(labels):
    print(f"Ponto {i}: Latitude: {gps_pontos[i][0]}, Longitude: {gps_pontos[i][1]}, Timestamp: {gps_pontos[i][2]}, Cluster: {label}")
    
    

mapa = folium.Map(location=[latitudeCFGC, longitudeCFGC], zoom_start=15)

# Adicionando os pontos ao mapa com marcadores vermelhos em formato de círculo
for lat, lon in coordinates:
    folium.CircleMarker(
        location=[lat, lon],
        radius=5,  # Tamanho do círculo
        color='red',  # Cor da borda do círculo
        fill=True,  # Preencher o círculo
        fill_color='red',  # Cor do preenchimento
        fill_opacity=0.7  # Opacidade do preenchimento
    ).add_to(mapa)

# Salvando o mapa em um arquivo HTML
mapa.save("clusters_mapa.html")
mapa