import json

from docx import Document
from copy import deepcopy

from Controllers.Utilities.utility import (
    set_text,
    insert_simple_bullets,
    insert_labeled_bullets
)

# ------------------------
# EXPERIENCE BLOCK
# ------------------------
def insert_experience(doc, experiences):
    paras = doc.paragraphs

    for i, para in enumerate(paras):
        if "{{EXPERIENCE_BLOCK}}" in para.text:

            parent = para._element.getparent()
            idx = parent.index(para._element)

            title_template = paras[i + 1]
            bullet_template = paras[i + 2]
            project_title_template = paras[i + 3]
            project_bullet_template = paras[i + 4]

            for exp in experiences:
                # Title line
                title_text = f"{exp['title']} | {exp['company']} | {exp['location']} | {exp['time']}"
                title_p = deepcopy(title_template)
                set_text(title_p, title_text)
                parent.insert(idx, title_p._element)
                idx += 1

                # Main bullets
                for b in exp["bullets"]:
                    bullet_p = deepcopy(bullet_template)
                    set_text(bullet_p, b)
                    parent.insert(idx, bullet_p._element)
                    idx += 1

                # Optional project section
                if exp.get("projects"):
                    proj_title = deepcopy(project_title_template)
                    parent.insert(idx, proj_title._element)
                    idx += 1

                    for pb in exp["projects"]:
                        proj_b = deepcopy(project_bullet_template)
                        set_text(proj_b, pb)
                        parent.insert(idx, proj_b._element)
                        idx += 1

                # AFTER finishing one experience give newline spaces in between
                spacer = deepcopy(title_template)
                set_text(spacer, "")
                parent.insert(idx, spacer._element)
                idx += 1

            # cleanup
            parent.remove(para._element)
            parent.remove(title_template._element)
            parent.remove(bullet_template._element)
            parent.remove(project_title_template._element)
            parent.remove(project_bullet_template._element)

            break


# ------------------------
# PROJECT BLOCK
# ------------------------
def insert_projects(doc, projects):
    paras = doc.paragraphs

    for i, para in enumerate(paras):
        if "{{PROJECT_BLOCK}}" in para.text:

            parent = para._element.getparent()
            idx = parent.index(para._element)

            title_template = paras[i + 1]
            bullet_template = paras[i + 2]

            for proj in projects:
                title_p = deepcopy(title_template)
                set_text(title_p, proj["title"])
                parent.insert(idx, title_p._element)
                idx += 1

                for b in proj["bullets"]:
                    bullet_p = deepcopy(bullet_template)
                    set_text(bullet_p, b)
                    parent.insert(idx, bullet_p._element)
                    idx += 1

                # AFTER finishing one project give newline spaces in between
                spacer = deepcopy(title_template)
                set_text(spacer, "")
                parent.insert(idx, spacer._element)
                idx += 1

            parent.remove(para._element)
            parent.remove(title_template._element)
            parent.remove(bullet_template._element)

            break

# ----------------------------------------
# REPLACE SINGLE VALUE (FOCUS/THESIS TITLE)
# -----------------------------------------
def replace_single_value(doc, placeholder, value):
    # paragraphs
    for para in doc.paragraphs:
        if placeholder in para.text:
            full_text = "".join(run.text for run in para.runs)
            new_text = full_text.replace(placeholder, value)

            para.runs[0].text = new_text
            for run in para.runs[1:]:
                run.text = ""

    # tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if placeholder in para.text:
                        full_text = "".join(run.text for run in para.runs)
                        new_text = full_text.replace(placeholder, value)

                        para.runs[0].text = new_text
                        for run in para.runs[1:]:
                            run.text = ""
                            
def replace_single_value_old(doc, placeholder, value, direct_replace=False):
    for para in doc.paragraphs:
        if placeholder in para.text:
            if (direct_replace == True):
                #para.text = para.text.replace(placeholder, value) # IT WILL REMOVE ALL FONT-FORMATTING

                full_text = "".join(run.text for run in para.runs)

                if placeholder in full_text:
                    new_text = full_text.replace(placeholder, value)

                    # keep first run formatting
                    first_run = para.runs[0]
                    first_run.text = new_text

                    # clear remaining runs
                    for run in para.runs[1:]:
                        run.text = ""
                        
            else:
                for run in para.runs:
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, value)
            

            

# ------------------------
# REMOVE OPTIONAL SECTION
# ------------------------
def remove_section(doc, section_title):
    remove = False
    for para in doc.paragraphs:
        if section_title in para.text:
            remove = True

        if remove:
            p = para._element
            p.getparent().remove(p)

        if remove and "EDUCATION" in para.text:
            break