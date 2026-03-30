import sys
import json
from docx import Document
from copy import deepcopy
import json

from get_linkedin import scrape_job_description
from generate_docx import (
    replace_single_value, 
    insert_experience, 
    insert_projects, 
    remove_section
)

from utility import (
    set_text,
    insert_simple_bullets,
    insert_labeled_bullets
)

def generate_docx_cv(template_path, json_path, output_path):
    doc = Document(template_path)

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    insert_simple_bullets(doc, "{{SUMMARY_ITEM}}", data["summary"])
    insert_labeled_bullets(doc, "{{TECH_TITLE}}", data["tech"])
    insert_labeled_bullets(doc, "{{SKILL_TITLE}}", data["skills"])
    insert_simple_bullets(doc, "{{AWARDS_BULLET}}", data["awards"])

    insert_experience(doc, data["experience"])

    replace_single_value(doc, "{{FOCUS_REPLACE}}", data["education"]["focus"])
    replace_single_value(doc, "{{THESIS_REPLACE}}", data["education"]["thesis"])

    if data.get("projects"):
        insert_projects(doc, data["projects"])
    else:
        remove_section(doc, "OPEN-SOURCE PROJECTS")

    doc.save(output_path)

