import numpy as np
from sklearn.cluster import DBSCAN
import folium
from datetime import datetime, timedelta

'''

Nessa abordagem, usou-se DBSCAN para separar os pontos em clusters

'''

#Definindo coordenadas para teste
gps_pontos = []

latitudeEscola = -4.569038553893695
longitudeEscola = -44.61631006359516
timestampEscola = datetime(2024, 8, 30, 8, 30, 45)

gps_pontos.append((latitudeEscola,longitudeEscola,timestampEscola))




latitudeEscola2 = -4.569813308517742
longitudeEscola2 = -44.61622477643236
timestampEscola2 = datetime(2024, 8, 30, 8, 30, 45)

gps_pontos.append((latitudeEscola2,longitudeEscola2,timestampEscola2))



latitudeTrabalho = -4.581143
longitudeTrabalho = -44.580817
timestampTrabalho = datetime(2024, 8, 30, 16, 20, 45)

gps_pontos.append((latitudeTrabalho,longitudeTrabalho,timestampTrabalho))


latitudeTrabalho2 = -4.580863
longitudeTrabalho2 = -44.580924
timestampTrabalho2 = datetime(2024, 8, 30, 16, 40, 45)

gps_pontos.append((latitudeTrabalho2,longitudeTrabalho2,timestampTrabalho2))



latitudeCasa = -4.565148908640259
longitudeCasa = -44.61757713316441
timestampCasa = datetime.now()

gps_pontos.append((latitudeCasa,longitudeCasa,timestampCasa))




latitudeRuaCasa = -4.565109
longitudeRuaCasa = -44.617429
timestampRuaCasa = datetime(2024,9,1,20,15,30)

gps_pontos.append((latitudeRuaCasa,longitudeRuaCasa,timestampRuaCasa))

gps_pontos.append((-4.562584806227442, -44.614710747357094,timestampRuaCasa))
'''
def gerarPontos(latitude, longitude, start_time, interval_seconds, num_pontos):
    pontos = []
    current_time = start_time
    for _ in range(num_pontos):
        pontos.append((latitude, longitude, current_time))
        current_time += timedelta(seconds=interval_seconds)
    return pontos

'''
#latitude = -23.550520  
#longitude = -46.633308  
#start_time = datetime.now()  
#interval_seconds = 60  
#num_pontos = 5


#gps_pontos = gerarPontos(latitudeCFGC, longitudeCFGC, start_time, interval_seconds, num_pontos)





'''
for point in gps_pontos:
    print(f"Latitude: {point[0]}, Longitude: {point[1]}, Timestamp: {point[2]}")
'''




coordinates = np.array([(point[0], point[1]) for point in gps_pontos])

dbscan = DBSCAN(eps=0.001, min_samples=2) 
labels = dbscan.fit_predict(coordinates)


for i, label in enumerate(labels):
    print(f"Ponto {i}: Latitude: {gps_pontos[i][0]}, Longitude: {gps_pontos[i][1]}, Timestamp: {gps_pontos[i][2]}, Cluster: {label}")
    
cluster_colors = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'orange',
    4: 'purple',
    5: 'pink',
    -1: 'black'  # -1 é o rótulo para pontos de ruído, caso existam
}


mapa = folium.Map(location=[latitudeEscola, longitudeEscola], zoom_start=13)



for i, (lat, lon) in enumerate(coordinates):
    folium.CircleMarker(
        location=[lat, lon],
        radius=3,  
        color=cluster_colors[labels[i]],  
        fill=True, 
        fill_color=cluster_colors[labels[i]],    
        fill_opacity=0.4  
    ).add_to(mapa)
    


mapa.save("Mapeamento_simples/clusters_mapa.html")
mapa