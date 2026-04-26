import streamlit as st
import pickle
import numpy as np
 
st.set_page_config(page_title="Laptop Price Predictor", page_icon="💻", layout="wide")
 
# Load saved model and dataframe
df   = pickle.load(open('df.pkl', 'rb'))
pipe = pickle.load(open('pipe.pkl', 'rb'))
 
# Minimal CSS — only styles the button, no background overrides
st.markdown("""
<style>
    div.stButton > button {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)
 
# Title
st.title("💻 Laptop Price Predictor")
st.caption("Fill in the laptop specifications and click Predict to get an estimated price.")
st.divider()
 
# Input form — 3 columns
col1, col2, col3 = st.columns(3)
 
with col1:
    st.subheader("Brand & Category")
    company   = st.selectbox("Brand",            sorted(df['Company'].unique()))
    type_name = st.selectbox("Type",             df['TypeName'].unique())
    os        = st.selectbox("Operating System", df['os'].unique())
 
with col2:
    st.subheader("Processor & Memory")
    cpu_brand = st.selectbox("CPU",      df['Cpu brand'].unique())
    gpu_brand = st.selectbox("GPU",      df['Gpu brand'].unique())
    ram       = st.selectbox("RAM (GB)", [2, 4, 6, 8, 12, 16, 24, 32, 64], index=3)
 
with col3:
    st.subheader("Storage & Display")
    ssd         = st.selectbox("SSD (GB)",             [0, 8, 128, 256, 512, 1024])
    hdd         = st.selectbox("HDD (GB)",             [0, 128, 256, 512, 1024, 2048])
    touchscreen = st.selectbox("Touchscreen",          ["No", "Yes"])
    ips         = st.selectbox("IPS Display",          ["No", "Yes"])
    ppi         = st.number_input("PPI",               min_value=50,  max_value=350, value=150)
    weight      = st.number_input("Weight (kg)",       min_value=0.5, max_value=5.0, value=1.8, step=0.1)
 
st.divider()
 
# Centered predict button
_, btn_col, _ = st.columns([2, 1, 2])
with btn_col:
    predict = st.button("Predict Price", type="primary")
 
# Result
if predict:
    ts_val  = 1 if touchscreen == "Yes" else 0
    ips_val = 1 if ips == "Yes" else 0
 
    query = np.array([
        company, type_name, ram, weight,
        ts_val, ips_val, ppi,
        cpu_brand, hdd, ssd, gpu_brand, os
    ]).reshape(1, 12)
 
    predicted_price = int(np.exp(pipe.predict(query)[0]))
    low  = int(predicted_price * 0.92)
    high = int(predicted_price * 1.08)
 
    st.divider()
 
    res_col, sum_col = st.columns(2, gap="large")
 
    with res_col:
        st.metric(label="Estimated Price", value=f"₹ {predicted_price:,}")
        st.caption(f"Expected range:  ₹ {low:,}  –  ₹ {high:,}")
 
    with sum_col:
        storage_parts = []
        if ssd > 0: storage_parts.append(f"{ssd} GB SSD")
        if hdd > 0: storage_parts.append(f"{hdd} GB HDD")
        storage_str = " + ".join(storage_parts) if storage_parts else "None"
 
        st.markdown("**Your Configuration**")
        summary = {
            "Brand":   company,
            "Type":    type_name,
            "CPU":     cpu_brand,
            "GPU":     gpu_brand,
            "RAM":     f"{ram} GB",
            "Storage": storage_str,
            "Display": f"{ppi} PPI · {'IPS' if ips_val else 'Non-IPS'} · {'Touch' if ts_val else 'No Touch'}",
            "OS":      os,
            "Weight":  f"{weight} kg",
        }
        for key, val in summary.items():
            c1, c2 = st.columns([1, 2])
            c1.markdown(f"**{key}**")
            c2.markdown(val)
 