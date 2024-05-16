"""
    handling all API calls to be used in the chatbot
"""
import json
import requests
import streamlit as st
from pydantic import BaseModel

class EmotionReport(BaseModel):
    """data structure to represent an emotion report"""
    sad: float
    joy: float
    love: float
    anger: float
    fear: float
    surprise: float

class MentalDisorderReport(BaseModel):
    """data structure to represent a mental disorder report"""
    depression: float
    anxiety: float
    adhd: float
    ocd: float
    bipolar: float
    autism: float
    no_mental_disorder: float

class RelevantConversation(BaseModel):
    """data structure to represent a relevant conversation"""
    patient_message: str
    therapist_message: str

def send_message(message: str) -> str:
    """Sending an HTTP request to send a message to Eve"""
    url = st.secrets["api_url"] + 'chat/messages/'
    payload = {
        'content': message
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {st.secrets["patient_token"]}'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
    return response.json()['data']['content']


def get_sentiment_posture():
    
    url = st.secrets["api_url"] + 'users/patient/'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {st.secrets["patient_token"]}'
    }

    response = requests.get(url, headers=headers, timeout=20)
    return response.json()['data']['sentiment_posture']['score']

def get_message_report(message: str):
    url = st.secrets["api_url"] + 'message-sentiments/score-text/'
    payload = {
        'text': message
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {st.secrets["therapist_token"]}'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
    data= response.json()['data']

    return EmotionReport(**data['emotion']), MentalDisorderReport(**data['mental_disorders']), RelevantConversation(**data['relevant_conversation'])

class MentalTextReport(BaseModel):
    """data structure to represent a mental disorder report"""
    recommendations: str
    conversation_highlgihts: str

class MentalDisorderNumericReport(BaseModel):
    """data structure to represent a mental disorder report"""
    depression_score: float
    anxiety_score: float
    adhd_score: float
    ocd_score: float
    bipolar_score: float
    autism_score: float
    no_mental_disorder_score: float

class ReportStats(BaseModel):
    sentiment_score: float
    messages_covered: float

@st.cache_data
def get_patient_sentiment_report(report_id: int):

    url = st.secrets["api_url"] + f'sentiment-reports/{report_id}/'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {st.secrets["therapist_token"]}'
    }

    response = requests.get(url, headers=headers, timeout=20)
    data = response.json()['data']
    
    return int(data['pk']), MentalTextReport(recommendations=data['recommendations'], conversation_highlgihts=data['conversation_highlights']),\
          MentalDisorderNumericReport(no_mental_disorder_score=data['no_mental_disorder_score'], 
                                      depression_score=data['depression_score'],
                                      autism_score=data['autism_score'],
                                        bipolar_score=data['bipolar_score'],
                                        ocd_score=data['ocd_score'],
                                        adhd_score=data['adhd_score'],
                                        anxiety_score=data['anxiety_score']
                                      ),\
          ReportStats(sentiment_score=data['sentiment_score'], messages_covered=data['messages_covered'])

class MentalHealthReportResposne(BaseModel):
    id: int
    sentiment_score: float
    messages_covered: int
    patient_id: int

@st.experimental_fragment(run_every=60)
def list_sentiment_reports():
    url = st.secrets["api_url"] + 'sentiment-reports/'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {st.secrets["therapist_token"]}'
    }

    response = requests.get(url, headers=headers, timeout=20)
    # return response.json()['data']
    # for r in response.json()['data']:
    #     st.write(r)
    return[ MentalHealthReportResposne(id=r['pk'], sentiment_score=r['sentiment_score'], messages_covered=r['messages_covered'], patient_id=r['patient']['id']) for r in response.json()['data']['results']]