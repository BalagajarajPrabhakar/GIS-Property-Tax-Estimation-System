import folium


def create_base_map():

    m=folium.Map(
        location=[13.0827,80.2707],
        zoom_start=12
    )

    folium.LatLngPopup().add_to(m)

    return m



def create_highlight_map(lat,lon):

    m=folium.Map(
        location=[lat,lon],
        zoom_start=15
    )

    folium.Marker(
        [lat,lon],
        icon=folium.Icon(color="red",icon="home"),
        popup="Nearest Property"
    ).add_to(m)

    return m