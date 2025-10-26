# Input Library Yang Dibutuhkan
import folium   # Untuk Melakukan Visualisasi Data
import geopandas as gpd #Untuk Melakukan Proses Data Geospasial

# Input Data Yang Akan Kita Masukkan Di Volium
data = gpd.read_file('C:\Geosoftware\WEBGIS\Webgis Makassar\Layout\Sediment_YieldKC.shp')

# Melakukan Pengaturan Warna Sesuai Kelas Sedimentasinya
color_dictionary = {'Sangat Rendah':'darkgreen', 'Rendah':'green', 'Sedang':'yellow', 'Tinggi':'darkorange', 'Sangat Tinggi':'red'}

# Mengatur Tampilan Peta
def style_function(feature):
  sedimentasi = feature['properties']['Kelas']
  return {
      'fillColor': color_dictionary.get(sedimentasi, 'gray'),
      'color': 'black',
      'weight': 0.5,
      'fillOpacity' : 0.8
  }

# Melakukan Inputan Data
m = folium.Map(
  location=[-4.53, 119.70],
  zoom_start=11
  )

folium.GeoJson(
    data=data, 
    name= 'Hasil SWAT DAS Lisu',
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=['KECAMATAN','Klasifikas','Kelas'],
        aliases = ['Kecamatan', 'Sedimentasi Bulanan (Ton/Hektar)','Kelas Sedimentasi'],
    )
).add_to(m)

# Menambahkan Marker (Outlet SWAT yang Ditentukan)
folium.Marker(
    location=[-4.45374958,119.60175598], 
    popup='Lokasi Outlet DAS (-4.45374958,119.60175598)',       
    tooltip='Outlet DAS',
    icon=folium.Icon(
        color='blue',         
        icon='water',          
        prefix='fa')            
).add_to(m)

# Menambahkan Basemap Lain Kedalam Folium Yang Dibuat
folium.TileLayer('Cartodb dark_matter', attr='Map Tiles by Cartodb').add_to(m)
folium.TileLayer('OpenStreetMap', attr='Map Tiles by Cartodb').add_to(m)
folium.TileLayer('Cartodb Positron', attr='Map Tiles by Cartodb').add_to(m)

# Menambahkan Kontrol Layer
folium.LayerControl().add_to(m)


m.save("Sedimentasi Das Lisu.html")





