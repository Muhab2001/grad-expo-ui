from pyparsing import col
import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
from utils.api import get_patient_sentiment_report, list_sentiment_reports
from utils.state import ReportPageState

def reports_config():
    st.set_page_config(
    page_title="Reports",
     page_icon="📊",
     layout="wide"
)
    add_logo("static/cfe5def5eb3a01ab75bb8c6052a8106991213c8e0413aeccb95332e3.png", height=80)

def reports_header():
    colored_header(
    label="📊 Mental health reports",
    description="",

    color_name="green-70",
)
    st.subheader("Explore how therapists can be empowered with AI to generate reports from patient history to better understand patients needs before his next appointments!")

def view_report(state: ReportPageState, id: int):
    
    pk, text_report, mental_disorders, stats= get_patient_sentiment_report(report_id=id)
    
    state.update_current_report(pk, text_report, mental_disorders, stats)


@st.experimental_fragment()
def reports_list(state: ReportPageState):
    
    reports = list_sentiment_reports()

    for report in reports:
        with st.container(border=True):
            st.text(f"Patient #{report.patient_id}")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.subheader(f"#{report.id}")
            with col2:
                st.text(f"messages {report.messages_covered} 📧")
                st.text(f"sentiment {report.sentiment_score} {'🟢' if report.sentiment_score > 0.5 else '🔴'}")

            st.button("View more", use_container_width=True, on_click=lambda: view_report(state, report.id), key=f"view_report_{report.id}")

def report_details():
    
    if not st.session_state.current_report:
        st.info("Please select a report to view it here")
    else:
        st.subheader(f"Report #{st.session_state.current_report}")
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            st.metric(f"Sentiment {'🟢' if st.session_state.sentiment_score >= 0.5 else '🔴'}", value=st.session_state.sentiment_score)
        
        with col2:
            st.metric("Messages 📧", value=f"{int(st.session_state.messages_covered)}")

        with col3:
            with st.popover("Mental Disorder Report", use_container_width=True):
                        for key, val in st.session_state.mental_disorders.items():
                            st.progress(val, text=' '.join(key.split('_')[:(len(key.split('_'))-1)]))

        st.divider()
        st.subheader("Conversation Highlights")
        st.write(st.session_state.text_report['conversation_highlgihts'])
        st.divider()

        st.subheader("Recommendations")
        st.write(st.session_state.text_report['recommendations'])
