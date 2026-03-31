import json

def fix_cv_schema(data):
    # FIX top-level projects (object → required format)
    for proj in data.get("projects", []):
        if "bullets" not in proj:
            if "description" in proj:
                proj["bullets"] = [proj["description"]]
            else:
                proj["bullets"] = []

    # FIX experience.projects → MUST BE STRING LIST
    for exp in data.get("experience", []):
        fixed_projects = []

        for proj in exp.get("projects", []):
            if isinstance(proj, dict):
                # convert object → string
                if "title" in proj and "bullets" in proj:
                    combined = proj["title"] + ": " + " ".join(proj["bullets"])
                elif "description" in proj:
                    combined = proj["description"]
                else:
                    combined = proj.get("title", "Project")

                fixed_projects.append(combined)

            elif isinstance(proj, str):
                fixed_projects.append(proj)

        exp["projects"] = fixed_projects

    return data