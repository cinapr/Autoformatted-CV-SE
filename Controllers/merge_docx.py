import os
import re
from docx import Document
from docxcompose.composer import Composer
from docx.enum.section import WD_SECTION

from Controllers.Utilities.utility import load_file, save_text, multi_line_input_INPUTFINISH_skipENTER, clean_xml_text, clean_dict

def merge_documents(cv_path, cl_path, scrap_txt_path, final_output_path):

    # ------------------------
    # 1. MERGE CV + COVER LETTER (STRICT PRESERVATION)
    # ------------------------
    master = Document(cv_path)
    composer = Composer(master)

    if os.path.exists(cl_path):
        composer.append(Document(cl_path))

    composer.save(final_output_path)

    # ------------------------
    # 2. ADD NEW SECTION FOR SCRAP TEXT
    # ------------------------
    doc = Document(final_output_path)

    # IMPORTANT: create a NEW SECTION (not just page break)
    new_section = doc.add_section(WD_SECTION.NEW_PAGE)

    # Optional: normalize layout for 3rd page (safe default)
    new_section.page_height = doc.sections[0].page_height
    new_section.page_width = doc.sections[0].page_width

    doc.add_heading('LinkedIn Job Description & Result', 1)

    if os.path.exists(scrap_txt_path):
        with open(scrap_txt_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    doc.add_paragraph(clean_xml_text(line.strip()))
                except Exception as e:
                    print(f"Failed line: {line}")
                    print(f"Exception: {e}")

    doc.save(final_output_path)

    print(f"✅ Final document created: {final_output_path}")