import math
import pandas as pd
import streamlit as st

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

st.title('H2S Removal Vessel Parameter Calculator')

diameter_ft = st.number_input('Vessel Diameter (ft)', value=8.0)
height_ft = st.slider('Vessel Height (ft)', min_value=16, max_value=40, value=20)
flow_rate_mmscfd = st.number_input('Flow Rate (MMSCFD)', value=30.0)
pressure_psig = st.number_input('Pressure (psig)', value=1000.0)

sv = calculate_space_velocity(diameter_ft, height_ft, flow_rate_mmscfd, pressure_psig)
lv = calculate_linear_velocity(diameter_ft, flow_rate_mmscfd, pressure_psig)

st.write(f"### Space Velocity (SV): {sv:.2f} hr^-1")
st.write(f"### Linear Velocity (LV): {lv:.2f} feet per hour")

heights = range(16, 41)
sv_values = [calculate_space_velocity(diameter_ft, h, flow_rate_mmscfd, pressure_psig) for h in heights]
lv_values = [calculate_linear_velocity(diameter_ft, flow_rate_mmscfd, pressure_psig) for h in heights]

df = pd.DataFrame({
    'Height (ft)': heights,
    'Space Velocity (hr^-1)': sv_values,
    'Linear Velocity (ft/hr)': lv_values
})

st.write("### SV and LV for Different Heights")
st.write(df)
