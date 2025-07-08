
import streamlit as st
from PIL import Image
import os
from vision_ocr import extract_text
from corrector import correct_text
from image_feedback import annotate_image

st.set_page_config(page_title="Handwriting Grammar Corrector", layout="centered")

lang = st.sidebar.radio("언어 / Language", ("English", "한국어"))
model_choice = st.sidebar.selectbox("GPT Model", ["gpt-3.5-turbo", "gpt-4"])

if lang == "English":
    st.title("📝 Handwriting Grammar Corrector")
    upload_label = "Upload a handwriting image"
    extracted_label = "📜 Extracted Text"
    corrected_label = "✅ Corrected Text"
    better_label = "✨ Better Response"
    button_label = "Correct Grammar & Annotate"
    spinner_extract = "Extracting text..."
    spinner_correct = "Correcting with ChatGPT..."
    spinner_annotate = "Annotating Image..."
    caption_uploaded = "Uploaded Image"
    caption_annotated = "Annotated Image"
else:
    st.title("📝 손글씨 문법 교정기")
    upload_label = "손글씨 이미지 업로드"
    extracted_label = "📜 추출된 텍스트"
    corrected_label = "✅ 교정된 텍스트"
    better_label = "✨ 더 자연스러운 표현"
    button_label = "문법 교정 및 이미지 표시"
    spinner_extract = "텍스트를 추출 중..."
    spinner_correct = "ChatGPT로 문법 교정 중..."
    spinner_annotate = "이미지에 표시 중..."
    caption_uploaded = "업로드된 이미지"
    caption_annotated = "교정된 이미지"

uploaded_file = st.file_uploader(upload_label, type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption=caption_uploaded, use_column_width=True)

    with st.spinner(spinner_extract):
        extracted_text = extract_text(image)

    st.subheader(extracted_label)
    st.text_area(extracted_label, extracted_text, height=150)

    if st.button(button_label):
        with st.spinner(spinner_correct):
            corrected_text, suggestions, better_response = correct_text(extracted_text, model=model_choice)

        st.subheader(corrected_label)
        st.text_area(corrected_label, corrected_text, height=150)

        st.subheader(better_label)
        st.text_area(better_label, better_response, height=150)

        with st.spinner(spinner_annotate):
            annotated_img = annotate_image(image, suggestions)
            st.image(annotated_img, caption=caption_annotated, use_column_width=True)
