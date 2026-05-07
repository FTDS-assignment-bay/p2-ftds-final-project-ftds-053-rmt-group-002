import streamlit as st

st.set_page_config(
    page_title='A-Limit',
    page_icon="💳",
    layout='wide',
    initial_sidebar_state='expanded'
)

st.markdown("""
<style>
/* ===== MAIN APP ===== */
.stApp {
    background-color: #0F172A;
    color: white;
}

/* ===== MAIN CONTAINER ===== */
[data-testid="stAppViewContainer"] {
    background-color: #0F172A;
}

/* ===== HEADER ===== */
[data-testid="stHeader"] {
    background: transparent;
}

/* ===== GLOBAL TEXT ===== */
html, body, [class*="css"] {
    color: #E5E7EB;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: #0F172A;
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* sidebar text */
section[data-testid="stSidebar"] * {
    color: #E5E7EB;
}

/* selectbox */
div[data-baseweb="select"] {
    background-color: #111827 !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* sidebar padding */
section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* sidebar title */
.sidebar-title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 30px;
    color: white;
}

/* subtle glow */
section[data-testid="stSidebar"]::before {
    content: "";
    position: absolute;
    top: -100px;
    left: -100px;
    width: 250px;
    height: 250px;
    background: rgba(34,199,242,0.08);
    filter: blur(80px);
    border-radius: 50%;
}

</style>
""", unsafe_allow_html=True)

import eda
import prediction

st.sidebar.markdown("""
<div class='sidebar-title'>
    A-Limit
</div>
""", unsafe_allow_html=True)

page = st.sidebar.selectbox(
    'Select Page',
    ('EDA', 'Prediction')
)

if page == 'EDA':
    eda.run()
else:
    prediction.run()