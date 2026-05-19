import streamlit as st
from streamlit_folium import st_folium
import folium
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from folium.raster_layers import ImageOverlay
import os

st.set_page_config(layout="wide")

st.title("🌍 Mersin Climate Dashboard")
st.markdown("Interactive NDVI, LST, and Urban Heat Hotspot Analysis")

# ---------------------------------------------------
# FUNCTION TO CONVERT TIFF → PNG
# ---------------------------------------------------

def tif_to_png(tif_path, png_path, cmap):
    with rasterio.open(tif_path) as src:
        data = src.read(1)

        # Clean invalid values
        data = np.nan_to_num(data)

        # Normalize
        data_norm = (data - data.min()) / (data.max() - data.min())

        # Save colored image
        plt.imsave(png_path, data_norm, cmap=cmap)

        bounds = src.bounds

    return bounds

# ---------------------------------------------------
# CREATE PNG OVERLAYS
# ---------------------------------------------------

os.makedirs("assets", exist_ok=True)

ndvi_bounds = tif_to_png(
    "Data/Mersin_NDVI_2025.tif",
    "assets/ndvi.png",
    "YlGn"
)

lst_bounds = tif_to_png(
    "Data/Mersin_LST_2025.tif",
    "assets/lst.png",
    "inferno"
)

hotspot_bounds = tif_to_png(
    "Data/Mersin_Hotspots_2025.tif",
    "assets/hotspots.png",
    "Reds"
)

# ---------------------------------------------------
# CREATE MAP
# ---------------------------------------------------

m = folium.Map(
    location=[36.8, 34.6],
    zoom_start=9,
    tiles="OpenStreetMap"
)

# ---------------------------------------------------
# NDVI LAYER
# ---------------------------------------------------

ImageOverlay(
    name="NDVI",
    image="assets/ndvi.png",
    bounds=[
        [ndvi_bounds.bottom, ndvi_bounds.left],
        [ndvi_bounds.top, ndvi_bounds.right]
    ],
    opacity=0.6
).add_to(m)

# ---------------------------------------------------
# LST LAYER
# ---------------------------------------------------

ImageOverlay(
    name="LST Heatmap",
    image="assets/lst.png",
    bounds=[
        [lst_bounds.bottom, lst_bounds.left],
        [lst_bounds.top, lst_bounds.right]
    ],
    opacity=0.6
).add_to(m)

# ---------------------------------------------------
# HOTSPOT LAYER
# ---------------------------------------------------

ImageOverlay(
    name="Urban Hotspots",
    image="assets/hotspots.png",
    bounds=[
        [hotspot_bounds.bottom, hotspot_bounds.left],
        [hotspot_bounds.top, hotspot_bounds.right]
    ],
    opacity=0.7
).add_to(m)

# ---------------------------------------------------
# LAYER CONTROL
# ---------------------------------------------------

folium.LayerControl().add_to(m)

# ---------------------------------------------------
# DISPLAY MAP
# ---------------------------------------------------

st_data = st_folium(
    m,
    width=1200,
    height=700
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("📊 Project Insights")

st.sidebar.markdown("""
### Key Findings

- NDVI-LST correlation: -0.19
- ML Model R²: 0.2049
- Neighborhood canopy effect: 43.3%
- Coastal/elevation effect: 46.2%

### Scientific Insight
Urban cooling in Mersin is a network effect driven by continuous vegetation corridors rather than isolated trees.
""")