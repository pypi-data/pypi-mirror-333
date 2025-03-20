from os.path import join, dirname

import streamlit as st
import streamlit.components.v1 as components


_RELEASE = True


if _RELEASE:
    root_dir = dirname(__file__)
    build_dir = join(root_dir, "frontend/build")

    _gps_location = components.declare_component(
        "gps_location",
        path=build_dir
    )
else:
    _gps_location = components.declare_component(
        "gps_location",
        url="http://localhost:3001/"
    )


if not _RELEASE:
    return_value = _gps_location()
    st.write("Return value:", return_value)
else:
    gps_location_button = _gps_location
