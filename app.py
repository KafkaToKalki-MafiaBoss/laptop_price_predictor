import streamlit as st
import pickle
import numpy as np

# Page config
st.set_page_config(page_title="Laptop Price Predictor", layout="centered")

# Load model
df = pickle.load(open('df.pkl', 'rb'))
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Simple CSS (clean, not overkill)
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}

.main {
    padding: 20px;
}

h1 {
    color: #2c3e50;
    text-align: center;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 10px;
    width: 100%;
}

.stButton>button:hover {
    background-color: #45a049;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("💻 Laptop Price Predictor")

st.write("Enter laptop specifications below:")

# Inputs
company = st.selectbox("Brand", sorted(df['Company'].unique()))
type_name = st.selectbox("Type", df['TypeName'].unique())
os = st.selectbox("Operating System", df['os'].unique())

cpu_brand = st.selectbox("CPU", df['Cpu brand'].unique())
gpu_brand = st.selectbox("GPU", df['Gpu brand'].unique())
ram = st.selectbox("RAM (GB)", [2, 4, 6, 8, 12, 16, 24, 32, 64])

ssd = st.selectbox("SSD (GB)", [0, 128, 256, 512, 1024])
hdd = st.selectbox("HDD (GB)", [0, 128, 256, 512, 1024, 2048])

touchscreen = st.selectbox("Touchscreen", ["No", "Yes"])
ips = st.selectbox("IPS Panel", ["No", "Yes"])
ppi = st.number_input("PPI", 50, 350, 150)

weight = st.number_input("Weight (kg)", 0.5, 5.0, 2.0)

# Prediction
if st.button("Predict Price"):

    ts_val = 1 if touchscreen == "Yes" else 0
    ips_val = 1 if ips == "Yes" else 0

    query = np.array([company, type_name, ram, weight, ts_val, ips_val,
                      ppi, cpu_brand, hdd, ssd, gpu_brand, os]).reshape(1, 12)

    log_price = pipe.predict(query)[0]
    price = int(np.exp(log_price))

    # Result card
    st.markdown(f"""
    <div class="card">
        <h3>Estimated Price</h3>
        <h2 style="color:#4CAF50;">₹{price}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Config summary
    st.markdown(f"""
    <div class="card">
        <h4>Configuration</h4>
        <p><b>Brand:</b> {company}</p>
        <p><b>CPU:</b> {cpu_brand}</p>
        <p><b>RAM:</b> {ram} GB</p>
        <p><b>Storage:</b> {ssd}GB SSD + {hdd}GB HDD</p>
        <p><b>GPU:</b> {gpu_brand}</p>
        <p><b>OS:</b> {os}</p>
        <p><b>Weight:</b> {weight} kg</p>
    </div>
    """, unsafe_allow_html=True)