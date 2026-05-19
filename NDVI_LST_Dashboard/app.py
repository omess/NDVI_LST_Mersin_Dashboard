import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.raster_layers import ImageOverlay
import os

st.set_page_config(layout="wide")

st.title("🌍 Mersin Climate Dashboard")
st.markdown("Interactive NDVI, LST, and Urban Heat Analysis")

# ---------------------------------------------------
# PATHS
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ndvi_path = os.path.join(BASE_DIR, "assets", "ndvi.png")
lst_path = os.path.join(BASE_DIR, "assets", "lst.png")
hotspots_path = os.path.join(BASE_DIR, "assets", "hotspots.png")

# Spatial Bounds Configuration
spatial_bounds = [[36.0, 33.8], [37.3, 35.0]]

# ---------------------------------------------------
# SIDEBAR CONTROL INTERFACE
# ---------------------------------------------------
st.sidebar.header("🗺️ Map Layer Controller")

# Using a selectbox guarantees the map doesn't crash from loading 3 massive arrays at once
layer_selection = st.sidebar.selectbox(
    "Choose Active Data Layer:",
    ["Base Map Only", "NDVI (Vegetation Index)", "LST Heatmap", "Urban Hotspots"]
)

# Opacity configuration dynamically linked to active layer
layer_opacity = st.sidebar.slider("Layer Opacity", min_value=0.1, max_value=1.0, value=0.6, step=0.1)

# ---------------------------------------------------
# MAP CONFIGURATION
# ---------------------------------------------------
m = folium.Map(
    location=[36.6, 34.4], # Centered tighter on your dataset bound
    zoom_start=9.5,
    tiles="OpenStreetMap"
)

# Dynamically inject layer ONLY if selected by the user
if layer_selection == "NDVI (Vegetation Index)":
    ImageOverlay(
        name="NDVI",
        image=ndvi_path,
        bounds=spatial_bounds,
        opacity=layer_opacity
    ).add_to(m)

elif layer_selection == "LST Heatmap":
    ImageOverlay(
        name="LST Heatmap",
        image=lst_path,
        bounds=spatial_bounds,
        opacity=layer_opacity
    ).add_to(m)

elif layer_selection == "Urban Hotspots":
    ImageOverlay(
        name="Urban Hotspots",
        image=hotspots_path,
        bounds=spatial_bounds,
        opacity=layer_opacity
    ).add_to(m)

# ---------------------------------------------------
# RENDER LAYOUT
# ---------------------------------------------------
# Display the dynamic map map
st_folium(m, width=1100, height=650, returned_objects=[])

# Project Statistics Section
st.sidebar.header("📊 Analytical Insights")
st.sidebar.markdown("""
### Model Metrics
- **NDVI-LST Correlation:** `-0.19`
- **ML Model R² Score:** `0.2049`
- **Neighborhood Canopy Weight:** `43.3%`
- **Coastal/Elevation Weight:** `46.2%`

> 💡 **Scientific Core:** Urban cooling across Mersin functions as an aggregate network layer. Continuous green corridors mathematically outperform disconnected landscape features.
""")
