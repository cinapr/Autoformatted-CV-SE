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

def generate_docx_coverletter(template_path, json_path, output_path):
    doc = Document(template_path)

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    replace_single_value(doc, "{{JOB_TITLE}}", data["jobtitle"])
    
    if data.get("hiringmanager"):
        replace_single_value(doc, "{{HIRING_MANAGER_NAME}}", data["hiringmanager"])
    else:
        remove_section(doc, "HIRING_MANAGER_NAME")

    if data.get("companyname"):
        replace_single_value(doc, "{{COMPANY_NAME}}", data["companyname"])
    else:
        remove_section(doc, "COMPANY_NAME")
    
    if data.get("companyaddress"):
        replace_single_value(doc, "{{COMPANY_ADDRESS}}", data["companyaddress"])
    else:
        remove_section(doc, "COMPANY_ADDRESS")

    if data.get("companylocation"):
        replace_single_value(doc, "{{COMPANY_LOCATION}}", data["companylocation"])
    else:
        remove_section(doc, "COMPANY_LOCATION")

    replace_single_value(doc, "{{BODY}}", data["coverletterbody"])


    doc.save(output_path)

