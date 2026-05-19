from bs4 import BeautifulSoup
import requests
import folium
from mapbook_lib.model import users

def get_coordinates(location: str) -> list:
    url = f"https://pl.wikipedia.org/wiki/{location}"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response_html = BeautifulSoup(response.text, 'html.parser')
    latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
    longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
    return [latitude, longitude]

def get_user_map(users_data: list) -> None:
    m = folium.Map([52.23, 21], zoom_start=6)


    for user in users_data:

        folium.Marker(
            location=get_coordinates(user["location"]),
            tooltip=user["name"],
            popup=user["posts"][-1],
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)


    m.save("mapa_znajomych.html")