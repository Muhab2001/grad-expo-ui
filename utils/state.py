
import streamlit as st
from typing import Dict, TypedDict
import pandas as pd

from utils.api import MentalDisorderNumericReport, MentalTextReport, ReportStats

class ChatMessage(TypedDict):
    """data structure to represent a chat message"""
    message: str
    sender: str
    avatar: str



def init_state_vars(initializers: Dict[str, any]):
    """function to be passed to the main app to initialize the state variables"""
    for key, value in initializers.items():

        if key not in st.session_state:
            st.session_state[key] = value

class ChatbotPageState:
    """class to handle all state management for the chatbot page"""

    def __init__(self, history_len: int = 6):
        
        init_state_vars({
            "message_list": [{
                "message": "Hey, how are you?",
                "sender": "Eve",
                "avatar": "static/eve_avatar.png"
            }],
            "previous_postures": [0, 0.5],
            "current_posture": 0.5,
            "message_counter": 0,
            "relevant_conversation": {},
            # "incoming_text": None
        })
        
        self.history_len = history_len

    def add_message(self, message: ChatMessage):
        messages_list = st.session_state.message_list
        st.session_state.message_list = messages_list[-self.history_len:] + [message]
        if message['sender'] == 'patient':
            print("Hello?")
            st.session_state.message_counter += 1

    def update_posture(self, new_posture: float):
        new_posture = float(new_posture)
        if new_posture != st.session_state.current_posture:
            # update current posture
            st.session_state.previous_posture = st.session_state.current_posture
            st.session_state.current_posture = float(new_posture)

            # update posture history
            previous_postures = st.session_state.previous_postures
            st.session_state.previous_postures = previous_postures[-self.history_len:] + [new_posture]
    
    def create_area_chart_df(self):
        data = st.session_state.previous_postures
        df = pd.DataFrame({
            "Sentiment posture": data,
            "index": range(len(data))
        })
        return df

    def update_relevant_conversation(self, patient_msg: str, therapist_msg: str):
        st.session_state.relevant_conversation = {
            "patient_msg": patient_msg,
            "therapist_msg": therapist_msg
        }

class ReportPageState:

    def __init__(self):
        init_state_vars({
            "current_report": None,
            "text_report": None,
            "mental_disorders": None,
            "sentiment_score": None,
            "messages_covered": None,
        })

    def update_current_report(self, report_id: int, text_report: MentalTextReport, mental_disorders: MentalDisorderNumericReport, stats: ReportStats):
        st.session_state.current_report = report_id
        st.session_state.text_report = text_report.model_dump()
        st.session_state.mental_disorders = mental_disorders.model_dump()
        st.session_state.sentiment_score = stats.sentiment_score
        st.session_state.messages_covered = stats.messages_covered