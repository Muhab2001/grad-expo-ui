import streamlit as st
from streamlit_extras.app_logo import add_logo

from streamlit_extras.colored_header import colored_header

def home_config():
    st.set_page_config(
    page_title="Home page",
     page_icon="🏠")
    add_logo("static/cfe5def5eb3a01ab75bb8c6052a8106991213c8e0413aeccb95332e3.png", height=80)

def home_header():

    colored_header(

    label="Jusoor Echo",
    description="",

    color_name="green-70",
)

    st.subheader("Join us to explore the capabilities of our mental health automated analysis and response pipeline that powers our system!")


def chatbot_section():

    with st.container():

        st.header("🤖 Eve the chatbot: Eliza's new little sister")
        st.markdown("""
### Discover how we created the next generation of Therapist Chatbots. Coming along way from Eliza's RegEx in 1960s to state-of-the-art LLMs, retrieval augmented generation, and post-processing resposne analysis. *Yup, that's Eve*!
""")
        st.page_link("pages/1_🤖_chatbot.py", label="Try Eve now!", icon="🔗", use_container_width=True)

    
def reports_section():
    
    with st.container():

        st.header("📊 Reports and analysis")
        st.markdown("""
### Dive into how we use LLMs to generate reports from patient history to better understand patients needs before his next appointments!
""")
        st.page_link("pages/2_📊_Reports.py", label="Explore reports", icon="🔗", use_container_width=True)