import streamlit as st

st.set_page_config(
    page_title = 'A-Limit',
    layout='wide',
    initial_sidebar_state='expanded'
)

import eda
import prediction
page = st.sidebar.selectbox('Select Page', ('EDA', 'Prediction'))

if page == 'EDA':
    eda.run()
else:
    prediction.run()