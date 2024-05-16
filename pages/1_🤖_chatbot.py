import streamlit as st
import time
# make_area from altair
# metrics
# chat input
# status for loading
# fragments directory
# cached API resposne
from components.chat import chat_message_area, chatbot_config, chatbot_description_header, user_sentiment_posture_tracker
from utils.state import ChatbotPageState

chatbot_config()

state = ChatbotPageState()

left_col, _, right_col = st.columns([2,0.2, 3])

with left_col:
    chatbot_description_header()
    user_sentiment_posture_tracker(state)

with right_col:
    chat_message_area(state)