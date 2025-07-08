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
    input_method = st.radio("Choose input method:", ["Upload image", "Take photo"])
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
    input_method = st.radio("입력 방식 선택:", ["이미지 업로드", "사진 촬영"])
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

with col1:
    if st.button("➕ Add student") and new_name:
        add_student(new_name)
        st.rerun()

with col2:
    if st.button("🗑️ Delete student") and student_name:
        students.remove(student_name)
        save_students(students)
        st.rerun()

model_choice = st.sidebar.selectbox("GPT Model", ["gpt-3.5-turbo", "gpt-4"], key="model_select")


st.title("📝 Handwriting Grammar Corrector")

input_method = st.radio("Choose input method:", ["Upload image", "Take photo"], key="input_method_radio")

uploaded_file = None
if input_method == "Upload image":
    uploaded_file = st.file_uploader("Upload or select image", type=["jpg", "jpeg", "png"])
elif input_method == "Take photo":
    uploaded_file = st.camera_input("Take a photo")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Input Image", use_container_width=True)

    with st.spinner("🔍 Extracting text..."):
        extracted_text = extract_text(image)

    st.subheader("📜 Extracted Text")
    st.text_area("Extracted Text", extracted_text, height=150)

    if st.button("✅ Correct Grammar"):
        with st.spinner("🤖 Correcting with ChatGPT..."):
            corrected_text, suggestions, _ = correct_text(extracted_text, model=model_choice)

        st.subheader("✅ Corrected Text")
        st.text_area("Corrected Text", corrected_text, height=150)

        st.subheader("💡 Suggested Version")
        st.text_area("Suggested Version", better_response, height=150)

        if student_name:
            save_history(student_name, extracted_text, corrected_text)

        # Download button
        download_txt = f"Student: {student_name}\n\nOriginal:\n{extracted_text}\n\nCorrected:\n{corrected_text}"
        st.download_button(
            label="💾 Download Feedback",
            data=download_txt,
            file_name=f"{student_name}_feedback.txt",
            mime="text/plain"
        )

        # Annotated image
        with st.spinner("🖍️ Annotating image..."):
            annotated_img = annotate_image(image, suggestions)
            st.image(annotated_img, caption="Annotated Image", use_container_width=True)

# Show history if student selected
if student_name:
    st.subheader(f"📚 History for {student_name}")
    history = load_history(student_name)
    if history:
        for item in reversed(history[-5:]):
            st.markdown(f"🕒 **{item['timestamp']}**")
            st.markdown(f"**OCR:** {item['ocr']}")
            st.markdown(f"**Corrected:** {item['corrected']}")
            st.markdown("---")
    else:
        st.info("No correction history yet for this student.")
