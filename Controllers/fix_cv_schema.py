import json

def fix_cv_schema(data):
    # Fix top-level projects
    if "projects" in data:
        fixed_projects = []
        for proj in data["projects"]:
            if isinstance(proj, str):
                fixed_projects.append({
                    "title": proj,
                    "bullets": []
                })
            else:
                if "bullets" not in proj:
                    proj["bullets"] = []
                fixed_projects.append(proj)
        data["projects"] = fixed_projects

    # Fix experience.projects (STRING EXPERIENCE.PROJECT)
    for exp in data.get("experience", []):
        if "projects" in exp:
            exp["projects"] = [
                proj if isinstance(proj, str) else proj.get("title", "")
                for proj in exp["projects"]
            ]

    return data