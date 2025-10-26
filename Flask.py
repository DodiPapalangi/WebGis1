from flask import Flask, render_template, request
import pandas as pd
import folium
import geopandas as gpd

app = Flask(__name__)

try:
    df_lisu = pd.read_csv("static/DasLisu.csv")
    unique_kecamatan = sorted(df_lisu['KECAMATAN'].unique().tolist())
    unique_kelas = sorted(df_lisu['Kelas'].unique().tolist())
except Exception as e:
    print(f"ERROR: Gagal memuat DasLisu.csv: {e}")
    df_lisu = pd.DataFrame({'KECAMATAN': [], 'Kelas': []})
    unique_kecamatan = []
    unique_kelas = []


@app.route("/", methods=["GET", "POST"])
def index():
    selected_kecamatan = request.form.get("filter_kecamatan", "Semua")
    selected_kelas = request.form.get("filter_kelas", "Semua")
    
    shapefile_path = r'C:\Geosoftware\WEBGIS\Webgis Makassar\Layout\Sediment_YieldKC.shp'
    data_geojson = gpd.GeoDataFrame()
    is_geojson_loaded = False
    error_message = None
    
    try:
        data_geojson = gpd.read_file(shapefile_path)
        is_geojson_loaded = True
    except Exception as e:
        error_message = f"ERROR: Gagal membaca shapefile: {e}. Cek jalur file."
        print(error_message)

    if is_geojson_loaded:
        filtered_geojson = data_geojson.copy()
        if selected_kecamatan != "Semua":
            filtered_geojson = filtered_geojson[
                filtered_geojson['KECAMATAN'] == selected_kecamatan
            ]
        
        if selected_kelas != "Semua":
            filtered_geojson = filtered_geojson[
                filtered_geojson['Kelas'] == selected_kelas
            ]
    else:
        filtered_geojson = gpd.GeoDataFrame()
    color_dictionary = {'Sangat Rendah':'darkgreen', 'Rendah':'green', 'Sedang':'yellow', 'Tinggi':'darkorange', 'Sangat Tinggi':'red'}
    
    def style_function(feature):
        sedimentasi = feature['properties'].get('Kelas', 'Unknown')
        return {
            'fillColor': color_dictionary.get(sedimentasi, 'gray'),
            'color': 'black',
            'weight': 0.5,
            'fillOpacity' : 0.8
        }
    m = folium.Map(
        location=[-4.53, 119.70],
        zoom_start=11,
        width='100%', 
        height='100%' 
    )

    if not filtered_geojson.empty:
        folium.GeoJson(
            data=filtered_geojson.to_json(), 
            name= 'Hasil SWAT DAS Lisu (Filter)',
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=['KECAMATAN','Klasifikas','Kelas'],
                aliases = ['Kecamatan', 'Sedimentasi Bulanan (Ton/Hektar)','Kelas Sedimentasi'],
            )
        ).add_to(m)

    folium.Marker(
        location=[-4.45374958,119.60175598], 
        popup='Lokasi Outlet DAS', 
        tooltip='Outlet DAS',
        icon=folium.Icon(
            color='blue', 
            icon='water', 
            prefix='fa')
    ).add_to(m)

    folium.TileLayer('Cartodb dark_matter', attr='Map Tiles by Cartodb').add_to(m)
    folium.TileLayer('OpenStreetMap', attr='Map Tiles by Cartodb').add_to(m)
    folium.TileLayer('Cartodb Positron', attr='Map Tiles by Cartodb').add_to(m)
    folium.LayerControl().add_to(m)

    map_html = m._repr_html_()
    return render_template("peta_swat_lisu.html", 
                           map_html=map_html,
                           unique_kecamatan=unique_kecamatan,
                           unique_kelas=unique_kelas,
                           selected_kecamatan=selected_kecamatan,
                           selected_kelas=selected_kelas,
                           error=error_message)

if __name__ == "__main__":
    app.run(debug=True)
