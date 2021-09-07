import folium
import pandas as pd
import webbrowser

# Load datasets
wonders_of_world_data = pd.read_csv("data/wonders_of_world.csv")
volcanoes_data = pd.read_csv("data/Volcanoes.txt")
file_name = "map.html"

# Pop Up Html for Wonders of world
pop_html = f"""<h4>%s</h4>
<p><a>%s</a></p>
<img src="%s"/>
"""


def color_selector(elv):
    """
        Color selector for volcano marker.
        Selects green color for marker if elevation of volcano is less than 1000.
        Selects orange color for marker if elevation of volcano is greater than equal to 1000 and less than 3000.
        Selects red if elevation is greater than 3000.
    """
    if elv < 1000:
        return 'green'
    elif 1000 <= elv < 3000:
        return 'orange'
    else:
        return 'red'


filtered_data = wonders_of_world_data[["Name", "Latitude",
                                       "Longitude", "Wikipedia link", "Picture link"]]

# Create a Map object
map = folium.Map(location=[wonders_of_world_data["Latitude"].iloc[0], wonders_of_world_data["Longitude"].iloc[0]],
                 zoom_start=2, tiles="OpenStreetMap", min_zoom=2)


# Create feature groups
fg_wonders = folium.FeatureGroup(name="Wonders Of World")

fg_volcanoes = folium.FeatureGroup(name="Volcanoes")

fg_population = folium.FeatureGroup(name="Population")

# Add markers to wonders of world group
for name, lat, long, wiki_link, pic_link in zip(filtered_data['Name'], filtered_data['Latitude'], filtered_data['Longitude'], filtered_data['Wikipedia link'], filtered_data['Picture link']):
    fg_wonders.add_child(folium.Marker(location=[
        lat, long], popup=pop_html % (name, wiki_link, pic_link), icon=folium.Icon(color='blue')))

# Add markers to volcano group
for name, lat, long, elv in zip(volcanoes_data['NAME'], volcanoes_data['LAT'], volcanoes_data['LON'], volcanoes_data['ELEV']):
    fg_volcanoes.add_child(folium.CircleMarker(location=[
        lat, long], popup=f'{name}\nElevation: {elv}', fill_color=color_selector(elv), color='grey', fill_opacity=0.7))

# Add color layer for population dataset
fg_population.add_child(folium.GeoJson(
    data=(open('data/world.json', 'r', encoding='utf-8-sig').read()),
    style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                              else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

# Add layers to map
map.add_child(fg_wonders)
map.add_child(fg_volcanoes)
map.add_child(fg_population)
map.add_child(folium.LayerControl())

# Save map
map.save(file_name)
webbrowser.open_new_tab(file_name)
