import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.raster_layers import ImageOverlay
import branca.colormap as cm
import plotly.express as px
import pandas as pd
import os

st.set_page_config(layout="wide")

st.title("🌍 Mersin Climate Intelligence Platform")
st.markdown("Advanced Spatial Optimization & Machine Learning Diagnostics")

# ---------------------------------------------------
# PATHS & CONFIGURATION
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ndvi_path = os.path.join(BASE_DIR, "assets", "ndvi.png")
lst_path = os.path.join(BASE_DIR, "assets", "lst.png")
hotspots_path = os.path.join(BASE_DIR, "assets", "hotspots.png")

spatial_bounds = [[36.0, 33.8], [37.3, 35.0]]

# ---------------------------------------------------
# SIDEBAR CONTROL INTERFACE
# ---------------------------------------------------
st.sidebar.header("🗺️ Map Settings")

# 1. Basemap Selection
basemap_choice = st.sidebar.selectbox(
    "Select Base Map Style:",
    ["Satellite Imagery", "CartoDB Dark Matter", "Standard OpenStreetMap"]
)

# 2. Data Layer Selection
layer_selection = st.sidebar.selectbox(
    "Active Analytical Layer:",
    ["None (Basemap Only)", "NDVI (Vegetation Index)", "LST Heatmap", "Urban Hotspots"]
)

layer_opacity = st.sidebar.slider("Layer Opacity", min_value=0.1, max_value=1.0, value=0.6, step=0.1)

# ---------------------------------------------------
# INITIALIZE MAP WITH CUSTOM BASEMAPS
# ---------------------------------------------------
# Map basemap choice to Folium tile providers
if basemap_choice == "Satellite Imagery":
    m = folium.Map(location=[36.6, 34.4], zoom_start=9.5, tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", attr="Esri")
elif basemap_choice == "CartoDB Dark Matter":
    m = folium.Map(location=[36.6, 34.4], zoom_start=9.5, tiles="CartoDB dark_matter")
else:
    m = folium.Map(location=[36.6, 34.4], zoom_start=9.5, tiles="OpenStreetMap")

# ---------------------------------------------------
# DYNAMICALLY INJECT DATA LAYERS & FLOATING LEGENDS
# ---------------------------------------------------
if layer_selection == "NDVI (Vegetation Index)":
    ImageOverlay(name="NDVI", image=ndvi_path, bounds=spatial_bounds, opacity=layer_opacity).add_to(m)
    # Add a custom floating NDVI colormap legend (Yellow to Green)
    legend = cm.LinearColormap(["#FFFFCC", "#C2E699", "#78C679", "#238443"], vmin=0.1, vmax=0.8, caption="NDVI (Vegetation Density)")
    legend.add_to(m)

elif layer_selection == "LST Heatmap":
    ImageOverlay(name="LST Heatmap", image=lst_path, bounds=spatial_bounds, opacity=layer_opacity).add_to(m)
    # Add a custom floating LST colormap legend (Inferno style: Blue to Red)
    legend = cm.LinearColormap(["#000004", "#781C6D", "#ED6925", "#FCFFA4"], vmin=20, vmax=45, caption="Land Surface Temp (°C)")
    legend.add_to(m)

elif layer_selection == "Urban Hotspots":
    ImageOverlay(name="Urban Hotspots", image=hotspots_path, bounds=spatial_bounds, opacity=layer_opacity).add_to(m)
    # Binary legend for risk zones
    legend = cm.StepColormap(["#G0G0G0", "#E31A1C"], vmin=0, vmax=1, caption="Critical Thermal Vulnerability Zone")
    legend.add_to(m)

# ---------------------------------------------------
# LAYOUT SPLIT: MAP VS GRAPHICS
# ---------------------------------------------------
col1, col2 = st.columns([3, 1.2]) # Create a wide column for map, narrower for charts

with col1:
    # Render map interface safely
    st_folium(m, width=900, height=650, returned_objects=[])

with col2:
    st.markdown("### 📊 ML Model Diagnostics")
    st.metric(label="Random Forest $R^2$ Fit", value="0.2049", delta="Validated Land Model")
    
    # Create interactive driver dominance dataframe
    df_features = pd.DataFrame({
        "Driver Metric": ["Distance to Sea", "Neighborhood Canopy", "Target Pixel NDVI"],
        "Importance (%)": [46.2, 43.3, 10.5]
    })
    
    # Build a clean interactive horizontal bar chart using Plotly Express
    fig = px.bar(
        df_features, 
        x="Importance (%)", 
        y="Driver Metric", 
        orientation='h',
        color="Importance (%)",
        color_continuous_scale="Viridis",
        template="plotly_dark"
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False, height=300, margin=dict(l=10, r=10, t=10, b=10))
    
    # Inject live chart into the dashboard grid layout
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    > **Urban Planning Takeaway:** Micro-climate resilience is an *aggregate network behavior*. Broad green networks drastically mitigate local pavement heat banking.
    """)
