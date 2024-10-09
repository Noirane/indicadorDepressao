import folium
import requests
import pandas as pd
from folium import GeoJson, GeoJsonTooltip
from branca.colormap import linear

# Carregar country_mapping
from country_data import country_mapping

# Configurar o Pandas para exibir todas as linhas
pd.set_option('display.max_rows', None)

# Função para criar o mapa
def create_map():
    world_map = folium.Map(
        location=[0, 0], 
        zoom_start=2, 
        tiles='http://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}.png', 
        attr='© CARTO'
    )
    
    # Carregar dados GeoJSON
    url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
    response = requests.get(url)
    geojson_data = response.json()

    return world_map, geojson_data

# Função para adicionar o GeoJson com base no índice de depressão
def add_geojson(map_obj, geojson_data, df):
    # Mapear o código numérico do país para o nome
    df['country_name'] = df['country'].map(country_mapping)
    
    # Calcular a média do índice de depressão por país
    country_depression = df.groupby('country_name')['indice_depressao'].mean().reset_index()
    
    # Criar um dicionário para facilitar a pesquisa por país
    depression_dict = country_depression.set_index('country_name')['indice_depressao'].to_dict()
    
    # Adicionar o índice de depressão ao objeto GeoJSON
    for feature in geojson_data['features']:
        country_name = feature['properties']['name']
        if country_name in depression_dict:
            feature['properties']['mean_depression_index'] = depression_dict[country_name]
        else:
            feature['properties']['mean_depression_index'] = None  # País sem participantes
    
    # Definir a faixa de valores para o colormap
    min_value = min(depression_dict.values(), default=0)
    max_value = max(depression_dict.values(), default=1)
    
    # Criar o colormap
    colormap = linear.YlOrRd_09.scale(min_value, max_value)
    
    # Adicionar o GeoJson com os estilos de cor baseados no índice de depressão
    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': (
                colormap(feature['properties'].get('mean_depression_index', 0))
                if feature['properties'].get('mean_depression_index') is not None else '#b4b49c'
            ),
            'color': 'black',  # Cor da borda dos países
            'weight': 1,
            'fillOpacity': 0.7 if feature['properties'].get('mean_depression_index') is not None else 0.3,
        },
        tooltip=GeoJsonTooltip(
            fields=['name', 'mean_depression_index'],
            aliases=['Country:', 'Average Depression Index:'],
            localize=True,
            sticky=True,
            labels=True,
            html='<div style="font-size: 14px;"><strong>Country:</strong> {name}<br><strong>Average Depression Index:</strong> {mean_depression_index:.2f}</div>'
        )
    ).add_to(map_obj)
    
    return map_obj

# Carregar o mapa e os dados GeoJSON
world_map, geojson_data = create_map()

# Carregar o dataset de índices de depressão
dataset_url = 'dataset.csv'  # Atualize para o caminho correto do seu arquivo
df = pd.read_csv(dataset_url)

# Verificar mapeamento e filtrar países que estão no GeoJSON
geojson_countries = {feature['properties']['name'] for feature in geojson_data['features']}
df['country_name'] = df['country'].map(country_mapping)
df = df[df['country_name'].isin(geojson_countries)]

# Adicionar o GeoJson e o tooltip
map_with_geojson = add_geojson(world_map, geojson_data, df)

# Configurar o colormap para criar a legenda personalizada
colormap = linear.YlOrRd_09.scale(df['indice_depressao'].min(), df['indice_depressao'].max())

def add_custom_legend(map_obj, colormap):
    # Definir os valores para a legenda
    legend_values = [colormap.vmin, colormap.vmin + (colormap.vmax - colormap.vmin) * 0.25,
                     colormap.vmin + (colormap.vmax - colormap.vmin) * 0.50,
                     colormap.vmin + (colormap.vmax - colormap.vmin) * 0.75, colormap.vmax]
    
    # Criar a faixa de cores para a legenda
    legend_colors = [colormap(val) for val in legend_values]
    
    # Criar uma legenda baseada no colormap
    legend_html = '''
    <div style="position: fixed; bottom: 20px; left: 20px; width: 220px; height: 100px; 
        background-color: rgba(0, 0, 0, 0.7); border:0px solid grey; 
        border-radius: 6px; z-index:9999; font-size:12px; color: white; padding: 8px;">
        <div style="text-align: center; font-weight: bold; margin-bottom: 5px;">Average Index Legend</div>
        <div style="margin-bottom: 5px;">
            <div style="width: 100%; height: 15px; background: linear-gradient(to right, {}); border-radius: 10px;"></div>
            <div style="display: flex; justify-content: space-between; width: 100%; margin-top: 5px;">
                <span>{:.0f}</span>
                <span>{:.0f}</span>
                <span>{:.0f}</span>
                <span>{:.0f}</span>
                <span>{:.0f}</span>
            </div>
        </div>
        <div style="margin-top: 10px;">
            <div style="width: 15px; height: 15px; background-color: #403438; display: inline-block; border: 1px solid black;"></div>
            <span style="margin-left: 5px;">Insufficient sample</span>
        </div>
    </div>
    '''.format(
        ', '.join(legend_colors),
        *legend_values
    )
    
    # Adicionar a legenda ao mapa
    map_obj.get_root().html.add_child(folium.Element(legend_html))

# Adicionar a legenda personalizada
add_custom_legend(map_with_geojson, colormap)

# Salvar o mapa
map_with_geojson.save('mapa_de_calor_com_legenda.html')
