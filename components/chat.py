import time
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_extras.app_logo import add_logo

from utils.api import get_message_report, get_sentiment_posture, send_message
from utils.state import ChatbotPageState
from utils.ui import typed_message
from streamlit_extras.colored_header import colored_header

def chatbot_config():
    st.set_page_config(
    page_title="Chatbot",
     page_icon="🤖",
     layout="wide"
)
    add_logo("static/cfe5def5eb3a01ab75bb8c6052a8106991213c8e0413aeccb95332e3.png", height=80)


def chatbot_description_header():

    colored_header(

    label="🤖Eve the chatbot",
    description="",
    color_name="green-70",
)
    st.markdown("This dashbboard demonstrates how Eve retrieves most similar theraapist resposne and uses it to guide its interactions. Also, we will showcase how our models can extract beneficial information from patient texts")
    with st.expander("👩‍💻 Technical Details"):
        st.markdown("""
    ### ChatBot
    Under the hood. Eve uses OpenAI's latest model GPT-4o on top of a RAG system using 🐘PostgreSQL
    vector search extension `pgvector` to lookup most similar conversations from a collected
    history of therapy sessions.
    
    ### Emotion and mental disorder detection
    Our team used 2 Distilled `TinyBERT` models that were pre-trained on wikipedia corpus for masked
    language models, and were also further fine-tuned on Stanford's sentiment tree bank dataset.

    ### Training Data collection
    The emotion dataset used a publicly-available data to extract emotion from Twitter's tweets. While
    the mental disorder dataset was collected from a dataset of Reddit's posts from mental health 
    support groups created by a survey research group from Harvard Medical school
    during COVID-19 pandemic. More details [here](https://zenodo.org/records/3941387#.Y8OqmtJBwUE)           
""")

@st.experimental_fragment(run_every=20)
def user_sentiment_posture_tracker(state: ChatbotPageState):

    last_posture = get_sentiment_posture()
    state.update_posture(last_posture)
    st.subheader("Sentiment Posture Tracker")

    left_col, right_col = st.columns([1, 3])
    
    with left_col.container(border=True, height=300):
        st.metric("Sentiment Posture", f"{float(st.session_state.current_posture):.2f}", f"{(float(st.session_state.current_posture) - float(st.session_state.previous_postures[-2])):.2f}%")
        st.metric("Message count", value=st.session_state.message_counter)

    with right_col.container(height=300):

        df = state.create_area_chart_df()
        st.area_chart(df, x="index", y = "Sentiment posture")   

@st.experimental_fragment
def chat_message_area(state: ChatbotPageState):
    
    
    with st.container(border=True, height=600):
        for message in st.session_state.message_list:
            with st.chat_message(message['sender'], avatar=message['avatar']):
                st.markdown(f"**{message['sender']}**")
                st.markdown(message['message'])
        if hasattr(st.session_state, 'incoming_text') and st.session_state.incoming_text:
            # optimistic update for UI
            patient_message = st.chat_message("patient", avatar="👨")
            patient_message.markdown("**patient**")
            patient_message.markdown(st.session_state.incoming_text)
            
            # update the state
            state.add_message({
                "avatar": "👨",
                "sender": "patient",
                "message": st.session_state.incoming_text
            })
            # optimistic update for UI for eve
            with st.chat_message("Eve", avatar="static/eve_avatar.png"):
                st.markdown("**Eve**")
                with st.spinner("Eve is typing..."):
                    response = send_message(st.session_state.incoming_text)
                typed_message(response)
                # update the state for eeve
                state.add_message({
                    "avatar": "static/eve_avatar.png",
                    "sender": "Eve",
                    "message": response
                })

            # TODO: API call to update the most relevant conversation
            ## as well as get the analysis for the message
            status = patient_message.status("Analyzing message...", expanded=False)
            emotion_report, disorder_report, relevant_conversation = get_message_report(st.session_state.incoming_text)
            state.update_relevant_conversation(relevant_conversation.patient_message, relevant_conversation.therapist_message)
            col1, col2 = patient_message.columns(2)
            with col1:
                with st.popover("Emotion Report", use_container_width=True):
                    for key, val in emotion_report.model_dump().items():
                        st.progress(val, text=key)
            with col2:
                with st.popover("Mental Disorder Report", use_container_width=True):
                    for key, val in disorder_report.model_dump().items():
                        st.progress(val, text=key)

            with patient_message.popover("Relevant conversation", use_container_width=True):
                with st.container(border=True):
                    st.markdown("**Patient**")
                    st.write(relevant_conversation.patient_message)
                with st.container(border=True):
                    st.markdown("**Therapist**")
                    st.write(relevant_conversation.therapist_message)

            status.update(state='complete')



    st.chat_input("Open up to eve!", key="incoming_text")
        