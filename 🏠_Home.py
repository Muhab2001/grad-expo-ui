import streamlit as st
from components.home import home_config, home_header, chatbot_section, reports_section
# You can access the value at any point with:

home_config()


home_header()
st.divider()
chatbot_section()
st.container(height=20, border=False) ## spacing out the sections
reports_section()
