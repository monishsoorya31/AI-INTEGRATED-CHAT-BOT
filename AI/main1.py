import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat Bot Using Machine Learning",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Load Google API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("Panimalar BOT 🍆")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.text_input("I'm Panimalar Bot. Type your message here:")

# Send user's message to Gemini-Pro and get the response
if st.button("Send"):
    st.session_state.chat_session.send_message(user_prompt)
    st.chat_message("user").markdown(user_prompt)

    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

# Define a video transformer class for audio processing
class AudioTransformer(VideoTransformerBase):
    def transform(self, frame):
        return frame

# Display the microphone input
webrtc_ctx = webrtc_streamer(key="audio", video_transformer_factory=AudioTransformer)
if webrtc_ctx.video_receiver:
    st.audio(webrtc_ctx.audio_receiver.audio_bytes, format="audio/ogg")
