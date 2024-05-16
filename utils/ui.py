import streamlit as st
import time

def typed_message(message: str):
    """display a message using a typing effect"""
    def generator(message: str):
        for letter in message:
            yield letter
            time.sleep(0.01)

    st.write_stream(generator(message))
