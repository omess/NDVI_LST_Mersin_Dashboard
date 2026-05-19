import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.raster_layers import ImageOverlay
import os

st.set_page_config(layout="wide")

st.title("🌍 Mersin Climate Dashboard")
st.markdown("Interactive NDVI, LST, and Urban Heat Analysis")

# ---------------------------------------------------
# DYNAMIC PATH RESOLUTION (Fixes FileNotFoundError)
# ---------------------------------------------------
# This finds the exact folder where app.py resides
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths to your assets
ndvi_path = os.path.join(BASE_DIR, "assets", "ndvi.png")
lst_path = os.path.join(BASE_DIR, "assets", "lst.png")
hotspots_path = os.path.join(BASE_DIR, "assets", "hotspots.png")

# Quick debug check for Streamlit logs to ensure paths look right
if not os.path.exists(ndvi_path):
    st.error(f"❌ Critical Error: Could not find NDVI asset at: {ndvi_path}")

# ---------------------------------------------------
# CREATE MAP
# ---------------------------------------------------
m = folium.Map(
    location=[36.8, 34.6],
    zoom_start=9,
    tiles="OpenStreetMap"
)

# ---------------------------------------------------
# NDVI OVERLAY
# ---------------------------------------------------
ImageOverlay(
    name="NDVI",
    image=ndvi_path,
    bounds=[
        [36.0, 33.8],
        [37.3, 35.0]
    ],
    opacity=0.6
).add_to(m)

# ---------------------------------------------------
# LST OVERLAY
# ---------------------------------------------------
ImageOverlay(
    name="LST Heatmap",
    image=lst_path,
    bounds=[
        [36.0, 33.8],
        [37.3, 35.0]
    ],
    opacity=0.6
).add_to(m)

# ---------------------------------------------------
# HOTSPOTS
# ---------------------------------------------------
ImageOverlay(
    name="Urban Hotspots",
    image=hotspots_path,
    bounds=[
        [36.0, 33.8],
        [37.3, 35.0]
    ],
    opacity=0.7
).add_to(m)

# ---------------------------------------------------
# CONTROLS
# ---------------------------------------------------
folium.LayerControl().add_to(m)

# ---------------------------------------------------
# DISPLAY
# ---------------------------------------------------
st_folium(m, width=1200, height=700)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("📊 Analysis")
st.sidebar.markdown("""
### Key Findings

- NDVI-LST correlation: -0.19
- ML Model R²: 0.2049
- Neighborhood canopy effect: 43.3%
- Coastal/elevation effect: 46.2%

### Scientific Insight
Urban cooling is driven by connected vegetation networks.
""")
