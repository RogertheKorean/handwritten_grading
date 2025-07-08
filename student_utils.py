
import json
import os
from datetime import datetime

STUDENT_FILE = "students.json"
HISTORY_DIR = "student_history"

def load_students():
    if not os.path.exists(STUDENT_FILE):
        return []
    with open(STUDENT_FILE, "r") as f:
        return json.load(f)

def save_students(student_list):
    with open(STUDENT_FILE, "w") as f:
        json.dump(student_list, f)

def add_student(name):
    students = load_students()
    if name not in students:
        students.append(name)
        save_students(students)

def save_history(student, ocr_text, corrected_text):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    filepath = os.path.join(HISTORY_DIR, f"{student}.json")
    history = []
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            history = json.load(f)
    entry = {
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "ocr": ocr_text,
        "corrected": corrected_text
    }
    history.append(entry)
    with open(filepath, "w") as f:
        json.dump(history, f)

def load_history(student):
    filepath = os.path.join(HISTORY_DIR, f"{student}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return []
