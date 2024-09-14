import numpy as np
from sklearn.cluster import DBSCAN
import folium
from geopy.distance import geodesic
from collections import defaultdict
from datetime import datetime
import random

'''
Essa abordagem, visou-se traçar um circulo a partir do ponto central do cluster gerado pelo DBSCAN

*** Verificar parâmetros do DBSCAN nos trabalhos

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


latitudeRuaVizinha = -4.5655453770115795
longitudeRuaVizinha = -44.61707380378729
timestampRuaVizinha = datetime(2024,9,1,20,30,30)

gps_pontos.append((latitudeRuaVizinha,longitudeRuaVizinha,timestampRuaVizinha))


latitudeRuaFora = -4.565970317059791
longitudeRuaFora = -44.61895133339691
timestampRuaFora = datetime(2024,9,1,20,30,30)

gps_pontos.append((latitudeRuaFora,longitudeRuaFora,timestampRuaFora))


coordinates = np.array([(point[0], point[1]) for point in gps_pontos])

dbscan = DBSCAN(eps=0.001, min_samples=1) 
labels = dbscan.fit_predict(coordinates)

# Dicionário para armazenar os pontos de cada cluster
clusters = defaultdict(list)
for i, label in enumerate(labels):
    clusters[label].append(coordinates[i])

# Calculando o centroide e o raio para cada cluster
centroides = {}
raios = {}
for label, points in clusters.items():
    # Centroide como a média das coordenadas
    centroide = np.mean(points, axis=0)
    centroides[label] = centroide
    
    # Raio como a máxima distância ao centroide
    max_dist = max([geodesic(centroide, point).meters for point in points])
    raios[label] = max_dist

# Criando o mapa
mapa = folium.Map(location=[latitudeEscola, longitudeEscola], zoom_start=13)

# Adicionando os pontos e círculos no mapa
for i, (lat, lon) in enumerate(coordinates):
    folium.CircleMarker(
        location=[lat, lon],
        radius=3,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.4
    ).add_to(mapa)

# Adicionando círculos ao redor dos centroides com o raio calculado
for label, centroide in centroides.items():
    folium.Circle(
        location=[centroide[0], centroide[1]],
        radius=raios[label], 
        color='blue',
        fill=True,
        fill_opacity=0.2
    ).add_to(mapa)

# Salvando o mapa
mapa.save("Mapeamento_com_DBSCAN_Circulo/clusters_com_circulos.html")