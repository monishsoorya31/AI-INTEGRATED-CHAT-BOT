from whisper_mic.whisper_mic import WhisperMic
import streamlit as st

mic = WhisperMic()
result = mic.listen()
st.write(result)