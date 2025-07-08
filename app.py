
import streamlit as st
from PIL import Image
import os
from vision_ocr import extract_text
from corrector import correct_text
from image_feedback import annotate_image
from student_utils import load_students, add_student, save_students, save_history, load_history
from io import StringIO

st.set_page_config(page_title="Handwriting Grammar Corrector", layout="centered")

# Load or create student list
students = load_students()

st.sidebar.header("👩‍🏫 Student Selection")
student_name = st.sidebar.selectbox("Select student", students)

new_name = st.sidebar.text_input("Add new student")
col1, col2 = st.sidebar.columns([1, 1])

with col1:
    if st.button("➕ Add student") and new_name:
        add_student(new_name)
        st.rerun()

with col2:
    if st.button("🗑️ Delete student") and student_name:
        students.remove(student_name)
        save_students(students)
        st.rerun()

model_choice = st.sidebar.selectbox("GPT Model", ["gpt-3.5-turbo", "gpt-4"])

st.title("📝 Handwriting Grammar Corrector")

input_method = st.radio("Choose input method:", ["Upload image", "Take photo"])

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
