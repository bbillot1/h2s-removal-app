import math
import pandas as pd
import streamlit as st

# Set page configuration
st.set_page_config(page_title="H2S Removal Vessel Calculator", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .main {background-color: #ffffff;}
        .block-container {padding: 2rem;}
        .stButton>button {background-color: #32CD32; color: #000000; border: none; border-radius: 4px; padding: 0.5rem 1rem; font-size: 1rem; cursor: pointer;}
        .stButton>button:hover {background-color: #228B22; color: #ffffff;}
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title('H2S Removal Vessel Parameter Calculator')
st.markdown("""
    **Welcome to the H2S Removal Vessel Parameter Calculator!**
    
    This app helps you calculate the space velocity (SV) and linear velocity (LV) for H2S removal vessels. 
    Adjust the inputs to see how they affect the performance of the vessel.
    
    **Instructions:**
    - **Vessel Diameter (ft):** The diameter of the vessel in feet.
    - **Vessel Height (ft):** The height of the vessel in feet.
    - **Flow Rate (MMSCFD):** The flow rate in million standard cubic feet per day.
    - **Pressure (psig):** The operating pressure in pounds per square inch gauge.
    
    The calculated **Space Velocity (SV)** and **Linear Velocity (LV)** will be displayed below.
""")

# Input fields
diameter_ft = st.number_input('Vessel Diameter (ft)', value=8.0, min_value=1.0)
height_ft = st.slider('Vessel Height (ft)', min_value=16, max_value=40, value=20)
flow_rate_mmscfd = st.number_input('Flow Rate (MMSCFD)', value=30.0, min_value=0.1)
pressure_psig = st.number_input('Pressure (psig)', value=1000.0, min_value=0.1)

# Calculation functions
def calculate_space_velocity(diameter_ft, height_ft, flow_rate_mmscfd, pressure_psig):
    volume_cubic_feet = math.pi * (diameter_ft / 2) ** 2 * height_ft
    actual_flow_rate_mmacfd = (flow_rate_mmscfd * 14.7) / (14.7 + pressure_psig)
    space_velocity = (actual_flow_rate_mmacfd * 1e6) / volume_cubic_feet
    return space_velocity

def calculate_linear_velocity(diameter_ft, flow_rate_mmscfd, pressure_psig):
    cross_sectional_area = math.pi * (diameter_ft / 2) ** 2
    actual_flow_rate_mmacfd = (flow_rate_mmscfd * 14.7) / (14.7 + pressure_psig)
    flow_rate_cfh = (actual_flow_rate_mmacfd * 1e6) / 24
    linear_velocity = flow_rate_cfh / cross_sectional_area
    return linear_velocity

# Calculate SV and LV
sv = calculate_space_velocity(diameter_ft, height_ft, flow_rate_mmscfd, pressure_psig)
lv = calculate_linear_velocity(diameter_ft, flow_rate_mmscfd, pressure_psig)

# Display results
st.markdown(f"### Results")
st.write(f"**Space Velocity (SV):** {sv:.2f} hr^-1")
st.write(f"**Linear Velocity (LV):** {lv:.2f} feet per hour")

# Create DataFrame for different heights
heights = range(16, 41)
sv_values = [calculate_space_velocity(diameter_ft, h, flow_rate_mmscfd, pressure_psig) for h in heights]
lv_values = [calculate_linear_velocity(diameter_ft, flow_rate_mmscfd, pressure_psig) for h in heights]

df = pd.DataFrame({
    'Height (ft)': heights,
    'Space Velocity (hr^-1)': sv_values,
    'Linear Velocity (ft/hr)': lv_values
})

# Display DataFrame
st.write("### SV and LV for Different Heights")
st.dataframe(df)

# Optional: Add a plot for better visualization
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:green'
ax1.set_xlabel('Height (ft)')
ax1.set_ylabel('Space Velocity (hr^-1)', color=color)
ax1.plot(df['Height (ft)'], df['Space Velocity (hr^-1)'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:black'
ax2.set_ylabel('Linear Velocity (ft/hr)', color=color)
ax2.plot(df['Height (ft)'], df['Linear Velocity (ft/hr)'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
st.pyplot(fig)
