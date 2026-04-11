import streamlit as st
import pickle
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LaptopIQ · Price Predictor",
    page_icon="💻",
    layout="wide",
)

# ── Load model ────────────────────────────────────────────────────────────────
df   = pickle.load(open('df.pkl', 'rb'))
pipe = pickle.load(open('pipe.pkl', 'rb'))

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
[data-testid="stHeader"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0a0a0f 0%, #12101e 40%, #0d1a2e 100%);
    border-bottom: 1px solid #1e1e30;
    padding: 56px 64px 40px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 360px; height: 360px;
    background: radial-gradient(circle, rgba(99,102,241,0.18) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(20,184,166,0.1) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #6366f1;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.25);
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(38px, 5vw, 62px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: #ffffff;
    margin-bottom: 16px;
}
.hero-title span {
    background: linear-gradient(90deg, #6366f1, #14b8a6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 15px;
    color: #6b7280;
    font-weight: 300;
    max-width: 480px;
    line-height: 1.7;
}

/* ── Main layout ── */
.main-wrap {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 0;
    min-height: calc(100vh - 220px);
}
.form-panel {
    padding: 48px 64px;
    border-right: 1px solid #1e1e30;
}
.result-panel {
    padding: 48px 40px;
    background: #0d0d16;
    display: flex;
    flex-direction: column;
    gap: 28px;
}

/* ── Section headers ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #1e1e30;
}

/* ── Grid rows ── */
.field-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 20px;
    margin-bottom: 32px;
}
.field-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 32px;
}

/* ── Selectboxes & inputs ── */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSlider"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #9ca3af !important;
    margin-bottom: 6px !important;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input {
    background: #111120 !important;
    border: 1px solid #1e1e30 !important;
    border-radius: 8px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stNumberInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

/* ── Toggle (Yes/No) styled selects ── */
.toggle-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 32px;
}

/* ── Predict button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 16px 24px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.35) !important;
    margin-top: 8px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.5) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Result card ── */
.result-card {
    background: linear-gradient(135deg, #12101e, #0d1a2e);
    border: 1px solid #1e1e30;
    border-radius: 16px;
    padding: 32px 28px;
    text-align: center;
}
.result-label {
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 10px;
    font-family: 'DM Mono', monospace;
}
.result-price {
    font-family: 'Syne', sans-serif;
    font-size: 48px;
    font-weight: 800;
    background: linear-gradient(90deg, #6366f1, #14b8a6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.result-range {
    font-size: 12px;
    color: #4b5563;
    margin-top: 8px;
    font-family: 'DM Mono', monospace;
}

/* ── Spec summary card ── */
.spec-card {
    background: #111120;
    border: 1px solid #1e1e30;
    border-radius: 12px;
    padding: 20px 22px;
}
.spec-card-title {
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 16px;
    font-family: 'DM Mono', monospace;
}
.spec-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #1a1a28;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
}
.spec-row:last-child { border-bottom: none; }
.spec-key { color: #4b5563; }
.spec-val { color: #e8e6f0; font-weight: 500; }

/* ── Stat pills ── */
.stat-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}
.stat-pill {
    background: #111120;
    border: 1px solid #1e1e30;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    font-family: 'DM Mono', monospace;
}
.stat-pill-val {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #6366f1;
}
.stat-pill-lbl {
    font-size: 10px;
    color: #4b5563;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-top: 4px;
}

/* ── Placeholder state ── */
.placeholder {
    background: #111120;
    border: 1px dashed #1e1e30;
    border-radius: 16px;
    padding: 40px 28px;
    text-align: center;
    color: #2d2d44;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    line-height: 1.8;
}
.placeholder-icon { font-size: 36px; margin-bottom: 12px; }

/* ── Divider ── */
.divider {
    height: 1px;
    background: #1e1e30;
    margin: 8px 0 28px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #1e1e30; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-tag">ML · Price Intelligence</div>
  <div class="hero-title">Laptop<span>IQ</span></div>
  <div class="hero-sub">Configure your specs below and get an instant AI-powered price estimate based on real market data.</div>
</div>
""", unsafe_allow_html=True)

# ── Layout: two columns ───────────────────────────────────────────────────────
col_form, col_result = st.columns([2.2, 1], gap="large")

with col_form:
    st.markdown('<div style="padding: 40px 0 0 0;">', unsafe_allow_html=True)

    # ── Brand & Type ──
    st.markdown('<div class="section-label">Brand & Category</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        company = st.selectbox("Brand", sorted(df['Company'].unique()))
    with c2:
        type_name = st.selectbox("Type", df['TypeName'].unique())
    with c3:
        os = st.selectbox("Operating System", df['os'].unique())

    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

    # ── Processor & Memory ──
    st.markdown('<div class="section-label">Processor & Memory</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        cpu_brand = st.selectbox("CPU", df['Cpu brand'].unique())
    with c2:
        gpu_brand = st.selectbox("GPU", df['Gpu brand'].unique())
    with c3:
        ram = st.selectbox("RAM (GB)", [2, 4, 6, 8, 12, 16, 24, 32, 64], index=3)

    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

    # ── Storage ──
    st.markdown('<div class="section-label">Storage</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        ssd = st.selectbox("SSD (GB)", [0, 8, 128, 256, 512, 1024])
    with c2:
        hdd = st.selectbox("HDD (GB)", [0, 128, 256, 512, 1024, 2048])

    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

    # ── Display ──
    st.markdown('<div class="section-label">Display</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        touchscreen = st.selectbox("Touchscreen", ["No", "Yes"])
    with c2:
        ips = st.selectbox("IPS Panel", ["No", "Yes"])
    with c3:
        ppi = st.number_input("PPI", min_value=50, max_value=350, value=150, step=1)

    st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

    # ── Physical ──
    st.markdown('<div class="section-label">Physical</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        weight = st.number_input("Weight (kg)", min_value=0.5, max_value=5.0, value=1.8, step=0.1)

    st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)

    predict_btn = st.button("⚡  Predict Price")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Right panel ───────────────────────────────────────────────────────────────
with col_result:
    st.markdown('<div style="padding: 40px 0 0 0;">', unsafe_allow_html=True)

    ts_val  = 1 if touchscreen == "Yes" else 0
    ips_val = 1 if ips == "Yes" else 0

    if predict_btn:
        query = np.array([company, type_name, ram, weight, ts_val, ips_val,
                          ppi, cpu_brand, hdd, ssd, gpu_brand, os]).reshape(1, 12)
        log_price = pipe.predict(query)[0]
        price     = int(np.exp(log_price))
        low       = int(price * 0.92)
        high      = int(price * 1.08)

        st.markdown(f"""
        <div class="result-card">
          <div class="result-label">Estimated Price</div>
          <div class="result-price">₹{price:,}</div>
          <div class="result-range">Range · ₹{low:,} – ₹{high:,}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

        # Spec summary
        storage_str = []
        if ssd > 0: storage_str.append(f"{ssd}GB SSD")
        if hdd > 0: storage_str.append(f"{hdd}GB HDD")
        storage_display = " + ".join(storage_str) if storage_str else "None"

        st.markdown(f"""
        <div class="spec-card">
          <div class="spec-card-title">Your Configuration</div>
          <div class="spec-row"><span class="spec-key">Brand</span><span class="spec-val">{company}</span></div>
          <div class="spec-row"><span class="spec-key">Type</span><span class="spec-val">{type_name}</span></div>
          <div class="spec-row"><span class="spec-key">CPU</span><span class="spec-val">{cpu_brand}</span></div>
          <div class="spec-row"><span class="spec-key">RAM</span><span class="spec-val">{ram} GB</span></div>
          <div class="spec-row"><span class="spec-key">Storage</span><span class="spec-val">{storage_display}</span></div>
          <div class="spec-row"><span class="spec-key">GPU</span><span class="spec-val">{gpu_brand}</span></div>
          <div class="spec-row"><span class="spec-key">Display</span><span class="spec-val">{ppi} PPI · {'IPS' if ips_val else 'Non-IPS'}</span></div>
          <div class="spec-row"><span class="spec-key">Touch</span><span class="spec-val">{'Yes' if ts_val else 'No'}</span></div>
          <div class="spec-row"><span class="spec-key">OS</span><span class="spec-val">{os}</span></div>
          <div class="spec-row"><span class="spec-key">Weight</span><span class="spec-val">{weight} kg</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

        # Quick stat pills
        st.markdown(f"""
        <div class="stat-row">
          <div class="stat-pill">
            <div class="stat-pill-val">₹{price//1000}K</div>
            <div class="stat-pill-lbl">Estimate</div>
          </div>
          <div class="stat-pill">
            <div class="stat-pill-val">{ram}GB</div>
            <div class="stat-pill-lbl">RAM</div>
          </div>
          <div class="stat-pill">
            <div class="stat-pill-val">{ssd if ssd > 0 else hdd}GB</div>
            <div class="stat-pill-lbl">Storage</div>
          </div>
          <div class="stat-pill">
            <div class="stat-pill-val">{weight}kg</div>
            <div class="stat-pill-lbl">Weight</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="placeholder">
          <div class="placeholder-icon">🖥</div>
          Configure your specs<br>on the left and hit<br><strong style="color:#6366f1">⚡ Predict Price</strong>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)