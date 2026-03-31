import json

def fix_cv_schema(data):
    # Fix top-level projects
    for proj in data.get("projects", []):
        if "bullets" not in proj:
            if "description" in proj:
                proj["bullets"] = [proj["description"]]
            else:
                proj["bullets"] = []

    # Fix experience.projects (if exists)
    for exp in data.get("experience", []):
        for proj in exp.get("projects", []):
            if isinstance(proj, str):
                # convert string project → bullets
                exp["projects"] = [{"title": "Project", "bullets": [proj]}]

    return data