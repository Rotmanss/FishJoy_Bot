import folium
from folium.plugins import MarkerCluster
import webbrowser
import os

from bot.father_bot import bot


def show_connections(locations, message):
    m = folium.Map(location=[locations[0]['lat'], locations[0]['lon']], zoom_start=2)

    # Add locations to the map
    marker_cluster = MarkerCluster().add_to(m)
    for loc in locations:
        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=loc['name'],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)

    # Create lines between consecutive points
    lines = [
        [[locations[i]['lat'], locations[i]['lon']], [locations[i + 1]['lat'], locations[i + 1]['lon']]]
        for i in range(len(locations) - 1)
    ]

    # Add lines to the map
    for line in lines:
        folium.PolyLine(locations=line, color='blue').add_to(m)

    # Save the map to an HTML file
    file_path = 'map.html'
    m.save(file_path)

    # Open the HTML file in the default web browser
    webbrowser.open('file://' + os.path.realpath(file_path))
    bot.send_message(chat_id=message.chat.id,
                     text="Here is the interactive map. Download the HTML file and open it in your browser.")

    # Send the HTML file as a document
    bot.send_document(chat_id=message.chat.id, document=open(file_path, 'rb'))
