from jsonschema import validate, ValidationError

CV_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {
            "type": "array",
            "items": {"type": "string"}
        },

        "experience": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "company": {"type": "string"},
                    "location": {"type": "string"},
                    "time": {"type": "string"},
                    "bullets": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "projects": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "bullets": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["title", "bullets"]
                        }
                    }
                },
                "required": ["title", "company", "location", "time", "bullets"]
            }
        },

        "projects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "bullets": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["title", "bullets"]
            }
        },

        "tech": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "value": {"type": "string"}
                },
                "required": ["title", "value"]
            }
        },

        "skills": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "value": {"type": "string"}
                },
                "required": ["title", "value"]
            }
        },

        "awards": {
            "type": "array",
            "items": {"type": "string"}
        },

        "education": {
            "type": "object",
            "properties": {
                "focus": {"type": "string"},
                "thesis": {"type": "string"}
            },
            "required": ["focus", "thesis"]
        }
    },

    "required": ["summary", "experience", "tech", "skills", "education"]
}

COVERLETTER_SCHEMA = {
    "type": "object",
    "properties": {
        "job_title": {"type": "string"},
        "company_name": {"type": "string"},
        "company_location": {"type": "string"},
        "hiring_manager_name": {"type": "string"},
        "company_address": {"type": "string"},
        "letter_date": {"type": "string"},
        "body": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["job_title", "company_name", "company_location", "body"]
}

CHECK_SCHEMA = {
    "type": "object",
    "properties": {
        "match_score": {"type": "number"},
        "is_suitable": {"type": "boolean"},
        "visa_sponsorship": {"type": "string"},
        "language_fit": {"type": "string"},
        "notes": {"type": "array", "items": {"type": "string"}},
        "missing_requirements": {"type": "array", "items": {"type": "string"}},
        "mandatory_documents": {"type": "array", "items": {"type": "string"}},
        "cover_letter_required": {"type": "boolean"}
    },
    "required": [
        "match_score",
        "is_suitable",
        "mandatory_documents",
        "cover_letter_required"
    ]
}

def validate_json(data, schema_type):
    try:
        if (schema_type=="CV"):
            validate(instance=data, schema=CV_SCHEMA)
            print("✅ JSON schema valid")
            return True
        elif (schema_type=="COVERLETTER"):
            validate(instance=data, schema=COVERLETTER_SCHEMA)
            print("✅ JSON schema valid")
            return True
        elif schema_type == "CHECK":
            validate(instance=data, schema=CHECK_SCHEMA)
            print("✅ JSON schema valid")
            return True
        else:
            print("❌ JSON schema INVALID")
            print("Error:schema type not defined - ", type)
            print("Path:schema.py")
            return False
    except ValidationError as e:
        print("❌ JSON schema INVALID")
        print("Error:", e.message)
        print("Path:", list(e.path))
        return False
    