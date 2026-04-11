import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Laptop Price Predictor", layout="centered")

# Load model
df = pickle.load(open('df.pkl', 'rb'))
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Minimal but good CSS
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: #e2e8f0;
}

h1 {
    text-align: center;
    color: #e2e8f0;
}

.block-container {
    padding-top: 2rem;
}

/* Inputs */
.stSelectbox, .stNumberInput {
    margin-bottom: 10px;
}

/* Button */
.stButton>button {
    background-color: #3b82f6;
    color: white;
    border-radius: 6px;
    padding: 10px;
    font-weight: 500;
}

.stButton>button:hover {
    background-color: #2563eb;
}

/* Cards */
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("💻 Laptop Price Predictor")

st.write("Fill the details and get estimated price")

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

# Predict
if st.button("Predict Price"):

    ts_val = 1 if touchscreen == "Yes" else 0
    ips_val = 1 if ips == "Yes" else 0

    query = np.array([company, type_name, ram, weight, ts_val, ips_val,
                      ppi, cpu_brand, hdd, ssd, gpu_brand, os]).reshape(1, 12)

    log_price = pipe.predict(query)[0]
    price = int(np.exp(log_price))

    st.markdown(f"""
    <div class="card">
        <h3>Estimated Price</h3>
        <h2 style="color:#3b82f6;">₹{price}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h4>Configuration</h4>
        <p>Brand: {company}</p>
        <p>CPU: {cpu_brand}</p>
        <p>RAM: {ram} GB</p>
        <p>Storage: {ssd}GB SSD + {hdd}GB HDD</p>
        <p>GPU: {gpu_brand}</p>
        <p>OS: {os}</p>
        <p>Weight: {weight} kg</p>
    </div>
    """, unsafe_allow_html=True)