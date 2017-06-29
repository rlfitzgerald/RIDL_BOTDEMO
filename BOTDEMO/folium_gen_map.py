import folium
import pdb
from folium.plugins import MarkerCluster # for marker clusters
import pandas as pd
import parseAIS
def _gen_map(lat,lon,markers,geojson,filename="default.html"):
	map_osm = folium.Map(location=[lat,lon],zoom_start=12)
	if geojson != None:
		G=folium.GeoJson(open(geojson))
		G.add_to(map_osm) 
	if markers != None:
		pass		
	map_osm.save(filename)
	return map_osm,filename

def _gen_map_locs(locs,filename="default.html"):
	map_osm = folium.Map(location=[33.747,-118.2103],zoom_start=14)
	marker_cluster = MarkerCluster(locations=locs,popups=locs)
	map_osm.add_children(marker_cluster)
	map_osm.save(filename)
	htmlfile = " ".join(open(filename).readlines())
	return htmlfile 

def _get_locs(filename):
	locs = parseAIS.parseAIS_coords("ais1.html")
	return locs

def mmap(lat,lon,geojson=None):
	map_file,filename=_gen_map(lat,lon,markers=None,geojson=geojson)
	f = " ".join(open(filename).readlines())
	print f	
	return f	
#	div,script=get_div_script(map_file)
#	div_string = str(div)	
#	script_string = str(script)	
#	return  div_string+script_string
def test():
	lat=33.734
	lon=-118.2373
	maps = mmap(lat,lon,geojson="/tmp/x.geojson")
	print maps
	#locs = _get_locs("shiplocs.csv")
	#print _gen_map_locs(locs)
