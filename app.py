import pandas as pd
from datetime import datetime

import streamlit as st
from PIL import Image
import os
from vision_ocr import extract_text
from corrector import correct_text
from image_feedback import annotate_image


import json


def export_user_history(user, history):
    if user not in history or not history[user]:
        return None
    records = []
    for i, entry in enumerate(history[user], 1):
        records.append({
            "Entry #": i,
            "Timestamp": entry.get("timestamp", ""),
            "Original Text": entry["original"],
            "Corrected Text": entry["corrected"],
            "Rewritten Text": entry.get("suggested", ""),
            "Explanation": entry.get("explanation", "")
        })
    return pd.DataFrame(records)


USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)


HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

users = load_users()

st.sidebar.markdown("### 👤 User Management")
selected_user = st.sidebar.selectbox("Select User", list(users.keys()) + ["➕ Add new user"], key="user_select")

if selected_user == "➕ Add new user":
    new_user = st.sidebar.text_input("Enter new username", key="new_user_input")
    if st.sidebar.button("Create User", key="create_user_btn") and new_user:
        users[new_user] = {}
        save_users(users)
        st.rerun()

delete_user = st.sidebar.selectbox("Delete User", list(users.keys()), key="delete_user")
if st.sidebar.button("Delete Selected User", key="delete_user_btn"):
    if delete_user in users:
        del users[delete_user]
        save_users(users)
        st.rerun()



st.markdown("## 📜 Full Correction History")
history = load_history()
if selected_user in history and history[selected_user]:
    for i, entry in enumerate(reversed(history[selected_user]), 1):
        with st.expander(f"📄 Entry #{i} | 🕒 {entry.get('timestamp', 'N/A')}"):
            st.markdown("**📝 Original Text**")
            st.code(entry["original"], language="text")

            st.markdown("**✅ Corrected Text**")
            st.code(entry["corrected"], language="text")

            if entry.get("suggested"):
                st.markdown("**💡 Rewritten Text**")
                st.code(entry["suggested"], language="text")

            if entry.get("explanation"):
                st.markdown("**🧠 GPT Explanation**")
                st.info(entry["explanation"])

    with st.expander("📤 Export Full History"):
        df = export_user_history(selected_user, history)
        if df is not None:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, f"{selected_user}_correction_history.csv", "text/csv")
        else:
            st.info("No history available to export.")
else:
    st.warning("No history found for this user.")

    st.sidebar.info("No history yet for this user.")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Current User:** `{selected_user}`")

st.set_page_config(page_title="Handwriting Grammar Corrector", layout="centered")

# Placeholder for user authentication (to be integrated)
# user = st.sidebar.text_input("User ID", key="user_id_input")

lang = st.sidebar.radio("언어 / Language", ("English", "한국어"), key="lang_radio")
model_choice = st.sidebar.selectbox("GPT Model", ["gpt-3.5-turbo", "gpt-4"], key="model_select")

if lang == "English":
    st.title("📝 Handwriting Grammar Corrector")
    input_method = st.radio("Choose input method:", ["Upload image", "Take photo"], key="input_method_radio")
    extracted_label = "📜 Extracted Text"
    corrected_label = "✅ Corrected Text"
    better_label = "💡 Suggested Version"
    button_label = "Correct Grammar & Annotate"
    spinner_extract = "Extracting text..."
    spinner_correct = "Correcting with ChatGPT..."
    spinner_annotate = "Annotating Image..."
    caption_uploaded = "Input Image"
    caption_annotated = "Annotated Image"
else:
    st.title("📝 손글씨 문법 교정기")
    input_method = st.radio("입력 방식 선택:", ["이미지 업로드", "사진 촬영"], key="input_method_radio_ko")
    extracted_label = "📜 추출된 텍스트"
    corrected_label = "✅ 교정된 텍스트"
    better_label = "💡 제안된 자연스러운 표현"
    button_label = "문법 교정 및 이미지 표시"
    spinner_extract = "텍스트를 추출 중..."
    spinner_correct = "ChatGPT로 문법 교정 중..."
    spinner_annotate = "이미지에 표시 중..."
    caption_uploaded = "입력된 이미지"
    caption_annotated = "교정된 이미지"

uploaded_file = None
if input_method in ["Upload image", "이미지 업로드"]:
    uploaded_file = st.file_uploader("Upload or select image", type=["jpg", "jpeg", "png"], key="image_upload")
elif input_method in ["Take photo", "사진 촬영"]:
    uploaded_file = st.camera_input("Take a photo", key="camera_capture")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption=caption_uploaded, use_container_width=True)

    with st.spinner(spinner_extract):
        extracted_text = extract_text(image)

    st.subheader(extracted_label)
    st.text_area(extracted_label, extracted_text, height=150)

    
    if st.button(button_label):
        with st.spinner(spinner_correct):
            corrected_text, suggestions, better_response = correct_text(extracted_text, model=model_choice)

        st.subheader(corrected_label)
        st.text_area(corrected_label, corrected_text, height=150)

        if better_response:
            st.subheader(better_label)
            st.text_area(better_label, better_response, height=150)

        with st.spinner(spinner_annotate):
            annotated_img = annotate_image(image, suggestions)
            st.image(annotated_img, caption=caption_annotated, use_container_width=True)

        # Save history per user
        history = load_history()

        entry = {
            "original": extracted_text,
            "corrected": corrected_text,
            "suggested": better_response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "explanation": "Corrected using GPT model for grammar accuracy and natural flow."
        }

        if selected_user not in history:
            history[selected_user] = []
        history[selected_user].append(entry)
        save_history(history)
        # Optionally save results to user history (to be added later)
        # save_to_history(user, extracted_text, corrected_text, better_response)
