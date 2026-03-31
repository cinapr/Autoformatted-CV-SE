import sys
import json
from docx import Document
from copy import deepcopy

from Controllers.Utilities.schema import validate_json
from Controllers.Utilities.generate_docx import (
    replace_single_value,
    remove_section
)

def generate_docx_coverletter(template_path, json_path, output_path):
    doc = Document(template_path)

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    if not validate_json(data, "COVERLETTER"):
        print("❌ Fix JSON before generating COVER LETTER")
        return

    # ------------------------
    # REQUIRED FIELDS
    # ------------------------
    replace_single_value(doc, "{{JOB_TITLE}}", data["job_title"])

    # ------------------------
    # OPTIONAL FIELDS (use consistent snake_case)
    # ------------------------
    if data.get("hiring_manager_name"):
        replace_single_value(doc, "{{HIRING_MANAGER_NAME}}", data["hiring_manager_name"])
    else:
        replace_single_value(doc, "{{HIRING_MANAGER_NAME}}", "")

    if data.get("company_name"):
        replace_single_value(doc, "{{COMPANY_NAME}}", data["company_name"])
    else:
        replace_single_value(doc, "{{COMPANY_NAME}}", "")

    if data.get("company_address"):
        replace_single_value(doc, "{{COMPANY_ADDRESS}}", data["company_address"])
    else:
        replace_single_value(doc, "{{COMPANY_ADDRESS}}", "")

    if data.get("company_location"):
        replace_single_value(doc, "{{COMPANY_LOCATION}}", data["company_location"])
    else:
        replace_single_value(doc, "{{COMPANY_LOCATION}}", "")

    if data.get("letter_date"):
        replace_single_value(doc, "{{LETTER_DATE}}", data["letter_date"])
    else:
        replace_single_value(doc, "{{LETTER_DATE}}", "")

    # ------------------------
    # BODY (array → paragraph)
    # ------------------------
    body_text = "\n\n".join(data.get("body", []))
    replace_single_value(doc, "{{BODY}}", body_text)

    # ------------------------
    # SAVE
    # ------------------------
    doc.save(output_path)
    print(f"✅ Cover letter generated: {output_path}")