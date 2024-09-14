import numpy as np
from sklearn.cluster import DBSCAN
import folium
from datetime import datetime, timedelta
import branca
from geopy import distance


'''
Essa abordagem visa traçar um buffer a partir de um ponto central



'''

#Definindo coordenadas para teste
gps_pontos = []
'''
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
'''


latitudeCasa = -4.565148908640259
longitudeCasa = -44.61757713316441
timestampCasa = datetime(2024, 9, 14, 8, 30, 45)

gps_pontos.append((latitudeCasa,longitudeCasa,timestampCasa))


#Adicionando pontos fora da área da casa (50m)
gps_pontos.append((-4.565037528718174, -44.61683020932483,datetime(2024, 9, 14, 8, 36, 45))) #63 metros
gps_pontos.append((-4.564774617279997, -44.61786034954978,datetime(2024,9,14,8,50,30))) #50.58 metros

#Adicionando pontos dentro da área da casa (50m)
gps_pontos.append((-4.564775818409348, -44.61766389641023,datetime(2024, 9, 14, 8, 33, 45))),   #43 metros
gps_pontos.append((-4.56555750197922, -44.61771374596735,datetime(2024, 9, 14, 8, 35, 45))),   #49 metros
gps_pontos.append((-4.564937677414269, -44.61734643034952,datetime(2024, 9, 14, 8, 47, 45))),   #49 metros

coordinates = np.array([(point[0], point[1]) for point in gps_pontos])


    
cluster_colors = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'orange',
    4: 'purple',
    5: 'pink',
    -1: 'black' 
}


mapa = folium.Map(location=[latitudeCasa, longitudeCasa], zoom_start=13)

pontosDentroCasa = []
pontosForaCasa = []
emCasa = False
tempoEmCasa = []

for i, (lat, lon) in enumerate(coordinates):
    
    if(distance.distance((latitudeCasa,longitudeCasa),(lat,lon)).m < 50):
        folium.CircleMarker(
            location=[lat, lon],
            radius=3,  
            color= 'green',  
            fill=True, 
            fill_color=False,    
            fill_opacity=0.4  
            
        ).add_to(mapa)
        
        if not emCasa:
            timestampInicio = gps_pontos[i][2]
            emCasa = True
        pontosDentroCasa.append((lat, lon, gps_pontos[i][2]))
        
        
    else:
         folium.CircleMarker(
            location=[lat, lon],
            radius=3,  
            color= 'red',  
            fill=True, 
            fill_color=False,    
            fill_opacity=0.4  
        ).add_to(mapa)
         
         if emCasa:
            emCasa = False
            timestampFim = gps_pontos[i][2]
            tempoEmCasa.append([timestampInicio,timestampFim])
         
         pontosForaCasa.append((lat, lon, gps_pontos[i][2]))    

#pontosDentroCasa = pontosDentroCasa.sort()
#pontosForaCasa = pontosForaCasa.sort()
folium.Circle(
    location=[latitudeCasa, longitudeCasa],
    radius=50,  # Raio em metros
    color='green',  
    fill=True,
    fill_color='blue',
    fill_opacity=0.2
).add_to(mapa)


print("Timestamps dos pontos dentro de casa:")
for ponto in pontosDentroCasa:
    print(f"Coordenadas: ({ponto[0]}, {ponto[1]}) - Timestamp: {ponto[2]}")


print(tempoEmCasa)
tempo_total_minutos = sum((fim - inicio).total_seconds() / 60 for inicio, fim in tempoEmCasa)
print(f"Tempo total gasto em casa: {tempo_total_minutos} minutos")



legend_html = '''
    <div style="position: fixed; 
                bottom: 10px; left: 10px; width: 150px; height: auto; 
                background-color: white; border:2px solid grey; z-index:9999; font-size:14px; padding:10px;">
        <b>Legenda</b><br>
        <i style="background: green; width: 12px; height: 12px; display: inline-block; border-radius: 50%;"></i> Casa <br>
        <i style="background: red; width: 12px; height: 12px; display: inline-block; border-radius: 50%;"></i> Escola<br>
        <i style="background: blue; width: 12px; height: 12px; display: inline-block; border-radius: 50%;"></i> Trabalho<br>
    </div>
'''


mapa.save("Mapeamento_Sem_DBSCAN/clusters_mapa.html")
mapa