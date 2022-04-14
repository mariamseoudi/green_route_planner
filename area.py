# from .elevations import
from enum import unique
import osmnx as ox
from shapely.geometry import Point,Polygon
import matplotlib.pyplot as plt
import networkx as nx
import geopandas as gp
import pandas as pd
import csv
from pyproj import Proj
from math import hypot
import pyproj
from shapely.geometry import shape
from shapely.ops import transform

import googlemaps
import requests
from urllib.parse import urlencode
from os.path import exists
from requests import get,post
ox.config(use_cache=True, log_console=True)
# get current weather data
def get_weather():
 url=f"http://api.openweathermap.org/data/2.5/air_pollution?lat=30.049999&lon=31.65&appid=d0715f9fcb74eba73da5d00ececdc6fb"
 url1=f'https://api.openweathermap.org/data/2.5/onecall?lat=30.049999&lon=31.65&units=metric&exclude=hourly,daily&appid=d0715f9fcb74eba73da5d00ececdc6fb'
 r = requests.get(url1)
 x=requests.get(url)
 if (r.status_code not in range(200, 299)): 
   return {}
 elif(x.status_code not in range(200, 299)):
     return {}
 weather={}
 try:
    
    uvi=r.json()['current']['uvi']
    visibility=r.json()['current']['visibility']
    wind_speed=r.json()['current']['wind_speed']
    aqi=x.json()['list'][0]['main']['aqi']
    weather={'uvi':uvi,'visibility':visibility,'wind_speed':wind_speed,'aqi':aqi}
 except:
        pass
 return weather
print(get_weather())
def polygon_to_utm(poly):
  s = shape(poly)
  wgs84 = pyproj.CRS('EPSG:4326')
  utm = pyproj.CRS('EPSG:32636')
  project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform
  project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform
  return(transform(project, s))
# a list of parks geometries is rturned in utm 
def getParks():
  tags = {'leisure': 'park', 'landuse': 'grass'}
  p = Proj(proj='utm',zone=36,ellps='WGS84', preserve_units=False)
  x1,y1 = p(31.4413,29.9868)#lon,lat 30.0186° N, 31.5015° E 29.9868° N, 31.4413° E

  x2,y2=p(31.4100, 30.0329)
  lon1,lat1=p(x1+10000,y1-10000,inverse=True)
  lon2,lat2=p(x1+10000,y2+10000,inverse=True)
  lon3,lat3=p(x2-10000,y1-100000,inverse=True)
  lon4,lat4=p(x2-10000,y2+10000,inverse=True)
  p1=[lon1,lat1]
  p2=[lon2,lat2]
  p3=[lon3,lat3]
  p4=[lon4,lat4]
# coords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)] 
  area=Polygon([p1,p2,p4,p3])
  parks =ox.geometries.geometries_from_polygon(area, tags)
  p=[]
  print(len(parks))
  for i in range(0,len(parks)):
    pol=parks['geometry'][i]

    p.append(polygon_to_utm(pol))
  return p
def getIndustrial():
  tags = {'landuse': 'industrial'}
  p = Proj(proj='utm',zone=36,ellps='WGS84', preserve_units=False)
  x1,y1 = p(31.4413,29.9868)#lon,lat 30.0186° N, 31.5015° E 29.9868° N, 31.4413° E

  x2,y2=p(31.4100, 30.0329)
  lon1,lat1=p(x1+10000,y1-10000,inverse=True)
  lon2,lat2=p(x1+10000,y2+10000,inverse=True)
  lon3,lat3=p(x2-10000,y1-100000,inverse=True)
  lon4,lat4=p(x2-10000,y2+10000,inverse=True)
  p1=[lon1,lat1]
  p2=[lon2,lat2]
  p3=[lon3,lat3]
  p4=[lon4,lat4]
# coords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)] 
  area=Polygon([p1,p2,p4,p3])
  parks =ox.geometries.geometries_from_polygon(area, tags)

  p=[]
  print(len(parks))
  for i in range(0,len(parks)):
    pol=parks['geometry'][i]

    p.append(polygon_to_utm(pol))
  return p
def createNetwork():
 p = Proj(proj='utm',zone=36,ellps='WGS84', preserve_units=False)
 x1,y1 = p(31.5015,30.0186)#lon,lat 30.0186° N, 31.5015° E

 x2,y2=p(31.4100, 30.0329)
# print(p(x1,y1,inverse=True))
# print((x1,y1))
# print((x2,y2))
 lon1,lat1=p(x1+10000,y1-10000,inverse=True)
 lon2,lat2=p(x1+10000,y2+10000,inverse=True)
 lon3,lat3=p(x2-10000,y1-100000,inverse=True)
 lon4,lat4=p(x2-10000,y2+10000,inverse=True)
 p1=[lon1,lat1]
 p2=[lon2,lat2]
 p3=[lon3,lat3]
 p4=[lon4,lat4]
# coords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)] 
 area=Polygon([p1,p2,p4,p3])
 G = ox.graph.graph_from_polygon(area, network_type='drive')
 return G
def possible_paths(G):

 edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
 nodes = ox.graph_to_gdfs(G, nodes=True, edges=False)
#  print(edges[edges.osmid==645457735])
 print(edges.loc[(29542602,7208831013 ,0  )]['geometry'])
#  print(G.edges[(29542602,7208831013 ,0  )]['length'])
#  print(G.edges[250642077])
 loc=ox.distance.nearest_nodes(G,31.4100, 30.0329 ,return_dist=False)
 des=ox.distance.nearest_nodes(G, 31.5015,30.0186 , return_dist=False)
 print((G.nodes[loc]['x'],G.nodes[loc]['y']))
 l=ox.distance.k_shortest_paths(G, loc, des,5, weight='length')
 i=0
 x=[]
 print(type(l))
 for p in l:
  i=i+1
  print(len(p))
  x.append(p)
 print (G.nodes[x[0][0]]["x"])
 print (G.nodes[x[0][0]]["y"])
 
 return x[1]
#  return(x)
#  ox.stats.count_streets_per_node(G,nodes=x[1])
#  unique_data = [list(p) for p in set(tuple(p) for p in x)]ox.utils_graph.get_route_edge_attributes(G, x[0], attribute=None, minimize_key='length'
#  print(len(unique_data))
# p = Proj(proj='utm',zone=36,ellps='WGS84', preserve_units=False)
# x1,y1 = p(31.5015,30.0186)#lon,lat 30.0186° N, 31.5015° E

# x2,y2=p(31.4413, 29.9868)
# dist = hypot(x2-x1, y2-y1)
# print(dist/1000)
# #
# pyproj.network.set_network_enabled(False)
graph=createNetwork()
streets=possible_paths(graph)
print(streets)


street_type=[]
ed=[] #edges geometry
lengths=[] #edges lengths
edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)
for i in range(0,len(streets)-1):
 e=edges.loc[(streets[i],streets[i+1],0  )]['geometry']
 l=edges.loc[(streets[i],streets[i+1],0  )]['length']
 s=edges.loc[(streets[i],streets[i+1],0  )]['highway']
 if(isinstance(s,list)):
   s=s[0]
 ed.append(e)
 lengths.append(l)
 street_type.append(s)

# print(ed)
# #############GVI############
p = Proj(proj='utm',zone=36,ellps='WGS84', preserve_units=False)
x1,y1 = p(31.4099858, 30.0330693)#lon,lat 30.0186° N, 31.5015° E
print(Point(x1,y1))
print(polygon_to_utm(ed[0]))
parks=getParks()
industries=getIndustrial()
t=[]#gvi cost
for line in ed:
  c=0
  shed=0
  line=polygon_to_utm(line)
  buffer=line.buffer(200)
  # print(buffer.intersects(parks[0]))
  # print(buffer.area)
# print(len(ed))

  for park in parks:
 
   if(buffer.intersects(park)):
    shed=shed+buffer.intersection(park).area
  # t.append((1-(shed/buffer.area)))
  t.append(1/((shed/buffer.area)+0.5))
print(t)
###############Elevations###########
def osmid_lonlat(graph,osmid):
  lon=graph.nodes[osmid]['x']
  lat=graph.nodes[osmid]['y']
  return(lon,lat)

def getElevations(x):
  (lon,lat)=x[0]
  s=str(lat)+","+str(lon)
  for i in range (1,len(x)):
      (lon,lat)=x[i]
      s=s+"|"+str(lat)+","+str(lon)
  
  endpoint = f"https://maps.googleapis.com/maps/api/elevation/json"
  params = {"locations":s, "key":'AIzaSyDtSGH4mC675HIpzM6o_JIvb8SNhv6c1Fs'}
  url_params = urlencode(params)
  url = f"{endpoint}?{url_params}"
  r = requests.get(url)
  if r.status_code not in range(200, 299): 
    return {}
  results=[]
  try:
       for i in range(0,len(r.json()['results'])):
         results.append(r.json()['results'][i]['elevation'])
  except:
          pass
  return results

nodes=[]
# streets
for r in streets:
 a=osmid_lonlat(graph,r)
 nodes.append(a)
n=getElevations(nodes) 
elev_cost=[] #elevation cost 
# n=[212.2237548828125, 212.2438659667969, 212.0391540527344, 211.7913818359375, 211.7509002685547, 211.2279663085938, 210.4700775146484, 210.2878875732422, 210.3863220214844, 211.1073760986328, 211.0530700683594, 211.8380432128906, 212.3641662597656, 212.7012786865234, 212.3901824951172, 212.1568145751953, 212.4109497070312, 213.1446380615234, 212.8714904785156, 212.6812438964844, 212.7747192382812, 213.7585601806641, 214.3841552734375, 214.2003326416016, 214.0169677734375, 213.2826843261719, 213.4331512451172, 218.4806518554688, 219.2827911376953, 219.8876495361328, 220.2129058837891, 218.2707366943359, 217.7973175048828, 218.2002105712891, 219.0562744140625, 220.2005615234375, 223.0004577636719, 224.7176513671875, 225.7500305175781, 225.8049011230469, 229.9269256591797, 229.8305816650391, 230.2519378662109, 230.6734924316406, 231.0794982910156, 233.2537689208984, 235.2547607421875, 235.251708984375, 234.3591003417969, 234.2345428466797, 236.1353302001953, 236.5839385986328, 236.9603729248047, 240.0224761962891, 250.3955688476562, 250.3301696777344, 248.36328125, 248.20166015625, 247.8014678955078, 248.0793914794922, 250.159423828125, 251.8153686523438, 254.6450653076172, 258.2430725097656, 258.9557189941406, 259.0082702636719, 252.7178497314453, 251.6377868652344, 245.2857360839844, 245.3620910644531, 246.5667877197266, 247.6602478027344, 249.2574768066406, 252.3687744140625, 253.1420135498047, 254.2493743896484, 255.2602233886719, 254.15576171875, 253.7957153320312, 254.7638854980469, 256.7816162109375, 258.9621276855469, 259.5959167480469, 259.8126220703125, 260.6996765136719, 266.1004333496094, 270.4926147460938, 271.7392578125, 272.0289916992188, 272.8113403320312, 277.060791015625, 277.9114379882812, 280.2667541503906, 280.2494506835938, 279.2824096679688, 279.2756958007812, 278.8539428710938, 278.2130126953125, 275.0511779785156, 275.255126953125, 277.5747680664062, 277.9559020996094, 281.8984069824219, 282.6273498535156, 291.1004943847656, 298.2323303222656, 300.2858276367188, 302.0040283203125, 302.7244567871094, 311.2628784179688, 311.4065551757812, 312.8370361328125, 317.798095703125, 318.4093933105469, 318.49755859375, 317.3575744628906, 317.1076049804688, 316.8606262207031, 320.2191772460938, 322.3501586914062, 322.2515563964844, 322.2742004394531, 322.3663635253906, 322.4216003417969]
# print(n)
for i in range(0,len(n)-1):
 r=0
 y=n[i+1]-n[i]
 x=lengths[i]
 slope=y/x
 if(slope<=0):
   r=0
 elif (slope>0.1):
      r=2
 else:
   r=slope*10
 elev_cost.append(r)
print(elev_cost)
 ################intersections#############
q=ox.stats.count_streets_per_node(graph, nodes=streets)
# print(streets)
# print(q)
intersection_cost=[]
for k in streets:
  count=q[k]
  if(count>3):
    intersection_cost.append(1)
  else:
     intersection_cost.append(0)
print(intersection_cost)  
################speed##################
speed_cost=[]

for s in street_type:
  r=0
  if(s=='motorway'):
   r=100
  elif(s=='motorway_link'):
   r=80
  elif(s=='trunk'):
   r=80
  elif(s=='trunk_link'):
   r=80
  elif(s=='primary'):
   r=60
  elif(s=='primary_link'):
   r=60
  elif(s=='secondary'):
   r=50
  elif(s=='secondary_link'):
   r=50
  speed_cost.append(r)
    
print(speed_cost)
######################air pollution##################
def green_areas_1000m(edges):
  t=[]
  for line in edges:
   c=0
  
   line=polygon_to_utm(line)
   buffer=line.buffer(1000)

   for park in parks:
 
    if(buffer.intersects(park)):
     c=c+1
   t.append(c)
  return t
print(green_areas_1000m(ed))
def industrial_areas_1000m(edges):
  t=[]
  for line in edges:
   c=0
  
   line=polygon_to_utm(line)
   buffer=line.buffer(1000)

   for ind in industries:
 
    if(buffer.intersects(ind)):
     c=c+1
   t.append(c)
  return t
print(industrial_areas_1000m(ed))