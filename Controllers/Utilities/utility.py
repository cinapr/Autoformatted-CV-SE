# utility.py
import sys
import json
from docx import Document
from copy import deepcopy


# ------------------------
# Load file
# ------------------------
def load_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# ------------------------
# Save text
# ------------------------
def save_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

# ------------------------
# Preserve formatting
# ------------------------
def set_text(paragraph, text):
    try:
        runs = paragraph.runs
        if runs:
            runs[0].text = text
            for r in runs[1:]:
                r.text = ""
        else:
            paragraph.add_run(text)

    except Exception as e:
        print("❌ ERROR in set_text")
        print(f"Paragraph object: {paragraph}")
        print(f"Text to insert: {text}")
        print(f"Error: {str(e)}")
        raise


# ------------------------
# SIMPLE BULLETS
# ------------------------
def insert_simple_bullets(doc, placeholder, items):
    for para in doc.paragraphs:
        if placeholder in para.text:
            parent = para._element.getparent()
            idx = parent.index(para._element)

            for item in items:
                new_p = deepcopy(para)
                set_text(new_p, item)
                parent.insert(idx, new_p._element)
                idx += 1

            parent.remove(para._element)
            break


# ------------------------
# LABELED BULLETS
# ------------------------
def insert_labeled_bullets(doc, placeholder, items):
    for para in doc.paragraphs:
        if placeholder in para.text:

            parent = para._element.getparent()
            idx = parent.index(para._element)

            for item in items:
                new_p = deepcopy(para)

                for r in new_p.runs:
                    r.text = ""

                run_title = new_p.runs[0]
                run_title.text = item["title"].upper() + ": "

                run_value = new_p.add_run(item["value"])

                template_run = para.runs[-1]
                run_value.font.name = template_run.font.name
                run_value.font.size = template_run.font.size
                run_value.bold = False

                parent.insert(idx, new_p._element)
                idx += 1

            parent.remove(para._element)
            break