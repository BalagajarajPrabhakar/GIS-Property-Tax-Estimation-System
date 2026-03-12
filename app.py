import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation

from tax_calculator import calculate_tax
from location_search import find_nearest_property
from map_utils import create_base_map,create_highlight_map


st.set_page_config(layout="wide")

st.title("GIS Property Tax Estimation System")


data=pd.read_csv("properties.csv")


tab1,tab2=st.tabs(["Estimate Tax from Map","Add New Property"])


# =================================
# TAB 1 : ESTIMATE TAX
# =================================

with tab1:

    st.header("Estimate Tax From Map")

    st.write("Click a location on the map")


    base_map=create_base_map()

    map_data=st_folium(
        base_map,
        width=700,
        height=500,
        key="estimate_map"
    )


    if map_data and map_data["last_clicked"]:

        lat=map_data["last_clicked"]["lat"]
        lon=map_data["last_clicked"]["lng"]

        st.write("Selected Location:",lat,lon)


        nearest=find_nearest_property(lat,lon,data)


        if nearest is not None:

            tax=calculate_tax(
                nearest["area_sqft"],
                nearest["zone"],
                nearest["type"]
            )


            st.subheader("Nearest Property Details")

            st.write("Property ID:",nearest["property_id"])
            st.write("Owner:",nearest["owner"])
            st.write("Area:",nearest["area_sqft"])
            st.write("Zone:",nearest["zone"])
            st.write("Type:",nearest["type"])


            st.success(f"Estimated Property Tax: ₹{tax}")


            highlight_map=create_highlight_map(
                nearest["latitude"],
                nearest["longitude"]
            )

            st.subheader("Nearest Property Location")

            st_folium(
                highlight_map,
                width=700,
                height=500,
                key="highlight_map"
            )



# =================================
# TAB 2 : ADD PROPERTY
# =================================

with tab2:

    st.header("Add New Property")


    method=st.radio(
        "Location Selection Method",
        ["Select on Map","Use Live Location"]
    )


    latitude=None
    longitude=None


    if method=="Select on Map":

        st.write("Click map to select location")

        add_map=create_base_map()

        map_data=st_folium(
            add_map,
            width=700,
            height=500,
            key="add_map"
        )


        if map_data and map_data["last_clicked"]:

            latitude=map_data["last_clicked"]["lat"]
            longitude=map_data["last_clicked"]["lng"]

            st.success(f"Selected Location: {latitude},{longitude}")


    if method=="Use Live Location":

        location=streamlit_geolocation()


        if location:

            latitude=location["latitude"]
            longitude=location["longitude"]

            st.success(f"Live Location: {latitude},{longitude}")


    st.subheader("Property Details")


    property_id=st.text_input("Property ID")

    owner=st.text_input("Owner Name")

    area=st.number_input("Area (sqft)",min_value=100)

    zone=st.selectbox("Zone",["A","B","C"])

    ptype=st.selectbox(
        "Property Type",
        ["residential","commercial","industrial"]
    )


    if st.button("Add Property"):

        if latitude and longitude:

            new_property={

                "property_id":property_id,
                "owner":owner,
                "area_sqft":area,
                "zone":zone,
                "type":ptype,
                "latitude":latitude,
                "longitude":longitude
            }


            data=pd.concat(
                [data,pd.DataFrame([new_property])],
                ignore_index=True
            )


            data.to_csv("data/properties.csv",index=False)


            st.success("Property Added Successfully")


        else:


            st.error("Please select a location first")
