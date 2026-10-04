
import json

import streamlit as st
from google import genai
from google.genai import types
from twilio.rest import Client as TwilioClient

from prompts import (
    SUMMARY_REQUEST_PROMPT,
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
)

# Use a currently supported vision-capable Gemini model.
# Verify model availability for your Google AI API key.
MODEL_NAME = "gemini-2.5-flash"

st.set_page_config(
    page_title="Snap & Study",
    page_icon="📚",
    layout="centered",
)

# API credentials stored in Streamlit secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TWILIO_ACCOUNT_SID = st.secrets["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = st.secrets["TWILIO_AUTH_TOKEN"]
TWILIO_WHATSAPP_FROM = st.secrets["TWILIO_WHATSAPP_FROM"]
TWILIO_CONTENT_SID = st.secrets["TWILIO_CONTENT_SID"]


@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


@st.cache_resource
def get_twilio_client():
    return TwilioClient(
        TWILIO_ACCOUNT_SID,
        TWILIO_AUTH_TOKEN,
    )


gemini_client = get_gemini_client()
twilio_client = get_twilio_client()


def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])

        elif message["kind"] == "image":
            st.image(message["content"], use_container_width=True)


def add_message(role, kind, content):
    message = {
        "role": role,
        "kind": kind,
        "content": content,
    }

    st.session_state.messages.append(message)
    render_message(message)


def ask_gemini(parts):
    try:
        response = st.session_state.chat.send_message(parts)
        return response.text or "I couldn't generate an explanation. Please try again."

    except Exception:
        st.error(
            "Sorry, I couldn't process your request. "
            "Please check your API configuration and try again."
        )
        return None


def clean_whatsapp_text(text):
    if not text:
        return "No study summary available."

    text = " ".join(text.split())

    # Keep the message within a reasonable size.
    return text[:1500] + "..." if len(text) > 1500 else text


def send_whatsapp(to_number, user_name, summary):
    # Twilio template placeholders:
    # {{1}} = student name
    # {{2}} = study summary

    try:
        content_variables = json.dumps(
            {
                "1": user_name,
                "2": clean_whatsapp_text(summary),
            },
            ensure_ascii=False,
        )

        message = twilio_client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{to_number}",
            content_sid=TWILIO_CONTENT_SID,
            content_variables=content_variables,
        )

        return True, message.sid

    except Exception:
        return False, (
            "The message could not be submitted. "
            "Please check your WhatsApp number and Twilio configuration."
        )


# --------------------------------------------------
# STEP 1: ONBOARDING
# --------------------------------------------------

if "onboarded" not in st.session_state:
    st.title("📚 Snap & Study")
    st.caption("Snap it. Understand it. Save it for later.")

    st.write(
        "Upload a photo of a question, diagram, textbook page, "
        "or handwritten notes. Get simple explanations and "
        "step-by-step solutions from your AI learning assistant."
    )

    with st.form("onboarding_form"):
        name = st.text_input(
            "Your name",
            placeholder="Enter your name",
        )

        whatsapp_number = st.text_input(
            "WhatsApp number (with country code)",
            placeholder="+91XXXXXXXXXX",
            help=(
                "This is the number Snap & Study will send "
                "your study summaries to."
            ),
        )

        submitted = st.form_submit_button(
            "Start Learning 🚀",
            use_container_width=True,
        )

    if submitted:
        if not name.strip() or not whatsapp_number.strip():
            st.warning("Please enter both your name and WhatsApp number.")

        else:
            st.session_state.name = name.strip()
            st.session_state.whatsapp_number = whatsapp_number.strip()

            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                ),
            )

            st.session_state.messages = []
            st.session_state.onboarded = True

            st.rerun()

    st.stop()


# --------------------------------------------------
# STEP 2: CHAT INTERFACE
# --------------------------------------------------

header_col, button_col = st.columns(
    [5, 2],
    vertical_alignment="center",
)

with header_col:
    st.title("📚 Snap & Study")

with button_col:
    # Enable summary sharing after at least one student
    # message and one assistant response.
    has_conversation = any(
        message["role"] == "user"
        for message in st.session_state.messages
    )

    send_disabled = not has_conversation

    if st.button(
        "📤 Send to WhatsApp",
        disabled=send_disabled,
        use_container_width=True,
    ):
        with st.spinner("Preparing your study summary..."):
            summary = ask_gemini([SUMMARY_REQUEST_PROMPT])

        if summary:
            success, info = send_whatsapp(
                st.session_state.whatsapp_number,
                st.session_state.name,
                summary,
            )

            if success:
                st.success("Study summary submitted to WhatsApp! 📲")
            else:
                st.error(info)


st.caption(
    f"Student: {st.session_state.name} | "
    f"WhatsApp: {st.session_state.whatsapp_number}"
)

# Show the welcome message once.
if not st.session_state.messages:
    add_message(
        "assistant",
        "text",
        WELCOME_MESSAGE_TEMPLATE.format(
            name=st.session_state.name
        ),
    )

else:
    for message in st.session_state.messages:
        render_message(message)


# --------------------------------------------------
# STEP 3: IMAGE AND TEXT INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Ask a question or upload a photo of your notes",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)

if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = (user_input.text or "").strip()

    parts = []

    # Process an uploaded image.
    if photo is not None:
        photo_bytes = photo.getvalue()

        add_message(
            "user",
            "image",
            photo_bytes,
        )

        parts.append(
            types.Part.from_bytes(
                data=photo_bytes,
                mime_type=photo.type,
            )
        )

    # Process the student's text.
    if text:
        add_message(
            "user",
            "text",
            text,
        )

        parts.append(text)

    elif photo is not None:
        parts.append(
            "Explain the educational content in this image "
            "in simple language. Identify the topic and provide "
            "a step-by-step explanation where appropriate. "
            "If the image is unclear, tell me what needs clarification."
        )

    # Ask Gemini to explain the content.
    if parts:
        with st.spinner("Understanding your question..."):
            answer = ask_gemini(parts)

        if answer:
            add_message(
                "assistant",
                "text",
                answer,
            )
