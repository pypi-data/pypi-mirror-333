import streamlit as st
from __init__ import _gps_location as gps_location

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run streamlit_gps_location/example.py`

# Define a function to handle location data
def process_location(location_data):
    if not location_data:
        st.write("No location data yet")

    if location_data.get("loading"):
        st.write("Loading location...")

    if location_data.get("latitude"):
        st.success("Location successfully retrieved!")
        st.write(f"Latitude: {location_data['latitude']}")
        st.write(f"Longitude: {location_data['longitude']}")
        st.write(f"Accuracy: {location_data['accuracy']} meters")
        
        # Display on a map
        map_data = {
            "lat": [location_data["latitude"]],
            "lon": [location_data["longitude"]]
        }
        st.map(map_data)
    
    # Show error if there was one
    if location_data.get("error"):
        st.error(f"Error getting location: {location_data['error']}")

# Get location with a custom button text
user_location = gps_location(
    buttonText="Get my location"
)

# Process location data when it changes
if user_location:
    process_location(user_location)
