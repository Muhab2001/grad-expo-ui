import streamlit as st
from components import reports
from components.reports import reports_config, reports_header, reports_list, report_details
from utils.api import get_message_report, get_patient_sentiment_report, list_sentiment_reports, send_message, get_sentiment_posture
from streamlit_extras.colored_header import colored_header

from utils.state import ReportPageState

state = ReportPageState()

reports_config()

col1, _, col2 = st.columns([1,0.5, 3])

with col1:
    reports_header()
    reports_list(state)

with col2:
    report_details()