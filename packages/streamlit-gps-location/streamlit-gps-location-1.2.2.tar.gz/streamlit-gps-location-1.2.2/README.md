# streamlit-gps-location

Streamlit component that allows you to get GPS location from browser

## Installation instructions

```sh
pip install streamlit-gps-location
```

## Usage instructions

```python
import streamlit as st

from streamlit_gps_location import gps_location_button

data = gps_location_button(
    buttonText="Get my location"
)

st.write(data)
```
