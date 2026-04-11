import streamlit as st
import pickle
import numpy as np

df = pickle.load(open('df.pkl', 'rb'))
pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title("💻 Laptop Price Predictor")

company = st.selectbox('Brand', df['Company'].unique())
type_name = st.selectbox('Type', df['TypeName'].unique())
ram = st.selectbox('RAM (GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
weight = st.number_input('Weight (kg)', 1.0, 4.0, step=0.1)
touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])
ips = st.selectbox('IPS Display', ['No', 'Yes'])
ppi = st.number_input('PPI (Pixels Per Inch)', 50, 300, value=150)
cpu_brand = st.selectbox('CPU Brand', df['Cpu brand'].unique())
hdd = st.selectbox('HDD (GB)', [0, 128, 256, 512, 1024, 2048])
ssd = st.selectbox('SSD (GB)', [0, 8, 128, 256, 512, 1024])
gpu_brand = st.selectbox('GPU Brand', df['Gpu brand'].unique())
os = st.selectbox('Operating System', df['os'].unique())

if st.button('Predict Price'):
    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips = 1 if ips == 'Yes' else 0

    query = np.array([company, type_name, ram, weight, touchscreen, ips,
                      ppi, cpu_brand, hdd, ssd, gpu_brand, os])
    query = query.reshape(1, 12)

    predicted_price = int(np.exp(pipe.predict(query)[0]))
    st.success(f"Estimated Laptop Price: ₹ {predicted_price:,}")