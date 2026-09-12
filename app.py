import streamlit as st
import streamlit.components.v1 as components
from dashboard_loader import build_dashboard

st.set_page_config(page_title='烘鞋器 · 品牌价格看板', page_icon='📊', layout='wide', initial_sidebar_state='collapsed')
st.markdown('<style>.block-container{padding:0.5rem 0.5rem 0}header[data-testid="stHeader"]{display:none}</style>', unsafe_allow_html=True)
components.html(build_dashboard(), height=1000, scrolling=True)
