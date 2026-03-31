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
                        "items": {"type": "string"}
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

COVERLETTER_SCHEMA = {}

def validate_json(data, type):
    try:
        if (type=="CV"):
            validate(instance=data, schema=CV_SCHEMA)
            print("✅ JSON schema valid")
            return True
        elif (type=="COVERLETTER"):
            validate(instance=data, schema=COVERLETTER_SCHEMA)
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