import json

from docx import Document
from copy import deepcopy

from Controllers.Utilities.utility import (
    set_text,
    insert_simple_bullets,
    insert_labeled_bullets
)


# ------------------------
# DEFINED SECTION HEADERS
# ------------------------
SECTION_HEADERS = [
    "PROFESSIONAL SUMMARY",
    "INDUSTRY EXPERIENCE",
    "TECHNICAL STACKS",
    "RELEVANT SKILLS",
    "OPEN-SOURCE PROJECTS",
    "EDUCATION",
    "AWARDS & CERTIFICATIONS"
]

# ------------------------
# EXPERIENCE BLOCK
# ------------------------
def insert_experience(doc, experiences):
    paras = doc.paragraphs

    title_template = None
    bullet_template = None
    project_title_template = None
    project_bullet_template = None
    block_index = None

    # खोज placeholders instead of fixed positions
    for i, para in enumerate(paras):
        text = para.text

        if "{{EXPERIENCE_BLOCK}}" in text:
            block_index = i

        elif "{{EXPERIENCE_TITLE_ITEM}}" in text:
            title_template = para

        elif "{{EXP_ITEM}}" in text:
            bullet_template = para

        elif "Projects:" in text:
            project_title_template = para

        elif "{{EXP_PROJECT_ITEM}}" in text:
            project_bullet_template = para

    if block_index is None:
        return

    parent = paras[block_index]._element.getparent()
    idx = parent.index(paras[block_index]._element)

    for exp in experiences:
        # Title
        title_text = f"{exp['title']} | {exp['company']} | {exp['location']} | {exp['time']}"
        title_p = deepcopy(title_template)
        set_text(title_p, title_text)
        parent.insert(idx, title_p._element)
        idx += 1

        # Bullets
        for b in exp.get("bullets", []):
            if not b.strip():
                continue
            bullet_p = deepcopy(bullet_template)
            set_text(bullet_p, b)
            parent.insert(idx, bullet_p._element)
            idx += 1

        # Projects (cleaned)
        projects = [
            p for p in exp.get("projects", [])
            if p and p.lower() not in ["titlebullets", "n/a", "none"]
        ]

        if projects:
            proj_title = deepcopy(project_title_template)
            parent.insert(idx, proj_title._element)
            idx += 1

            for pb in projects:
                proj_b = deepcopy(project_bullet_template)
                set_text(proj_b, pb)
                parent.insert(idx, proj_b._element)
                idx += 1

        # Spacer
        spacer = deepcopy(title_template)
        set_text(spacer, "")
        parent.insert(idx, spacer._element)
        idx += 1

    # Cleanup templates
    for t in [
        paras[block_index],
        title_template,
        bullet_template,
        project_title_template,
        project_bullet_template
    ]:
        if t is not None:
            parent.remove(t._element)
            
def insert_experience_old(doc, experiences):
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
def remove_section_project(doc, section_title):
    remove = False
    for para in doc.paragraphs:
        if section_title in para.text:
            remove = True

        if remove:
            p = para._element
            p.getparent().remove(p)

        if remove and "EDUCATION" in para.text:
            break

def remove_section_old(doc, section_title):
    import traceback, sys
    try:
        paras = doc.paragraphs
        start_idx = None

        # find section title
        for i, p in enumerate(paras):
            if section_title in p.text:
                start_idx = i
                break

        if start_idx is None:
            return

        # find end of section (next divider line or empty line block)
        end_idx = len(paras)
        for i in range(start_idx + 1, len(paras)):
            if "____" in paras[i].text:  # your section separator
                end_idx = i
                break

        # delete paragraphs in range
        for i in range(end_idx - 1, start_idx - 1, -1):
            p = paras[i]._element
            p.getparent().remove(p)

    except Exception as e:
        tb = traceback.extract_tb(sys.exc_info()[2])[-1]
        print(f"[ERROR] remove_section failed")
        print(f"Line: {tb.lineno} | File: {tb.filename}")
        print(f"Error: {str(e)}")



def remove_section(doc, section_title):
    import traceback, sys

    SECTION_HEADERS = [
        "PROFESSIONAL SUMMARY",
        "INDUSTRY EXPERIENCE",
        "TECHNICAL STACKS",
        "RELEVANT SKILLS",
        "OPEN-SOURCE PROJECTS",
        "EDUCATION",
        "AWARDS & CERTIFICATIONS"
    ]

    try:
        paras = doc.paragraphs
        start_idx = None

        # 1. find start
        for i, p in enumerate(paras):
            if section_title in p.text:
                start_idx = i
                break

        if start_idx is None:
            print(f"[INFO] Section not found: {section_title}")
            return

        # 2. find next section header ONLY (ignore separators completely)
        end_idx = len(paras)
        for i in range(start_idx + 1, len(paras)):
            text = paras[i].text.strip()

            # skip empty lines
            if not text:
                continue

            # 🚨 stop at next section header
            if any(header in text for header in SECTION_HEADERS if header != section_title):
                end_idx = i
                break

        print(f"[DEBUG] Removing '{section_title}' from {start_idx} to {end_idx}")

        # 3. delete only this section
        for i in range(end_idx - 1, start_idx - 1, -1):
            p = paras[i]._element
            p.getparent().remove(p)

    except Exception as e:
        tb = traceback.extract_tb(sys.exc_info()[2])[-1]
        print(f"[ERROR] remove_section failed")
        print(f"Line: {tb.lineno} | File: {tb.filename}")
        print(f"Error: {str(e)}")



        