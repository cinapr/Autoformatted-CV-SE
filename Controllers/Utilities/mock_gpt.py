import json

# ------------------------
# SIMULATE CHECK (JOB FIT)
# ------------------------
def simulate_check():
    return {
        "match_score": 85,
        "is_suitable": True,
        "visa_sponsorship": "Not mentioned",
        "language_fit": "OK",
        "notes": [
            "Strong alignment with Business Analyst role",
            "Experience matches requirements in systems and stakeholders"
        ],
        "missing_requirements": [
            "No explicit financial market experience mentioned"
        ],
        "mandatory_documents": [
            "CV",
            "Cover Letter"
        ],
        "cover_letter_required": True
    }


# ------------------------
# SIMULATE CV
# ------------------------
def simulate_cv():
    return {
        "summary": [
            "Business Analyst with experience in IT systems and stakeholder alignment",
            "Strong in requirements gathering and translating business needs",
            "Experienced in Agile delivery and system optimization"
        ],
        "experience": [
            {
                "title": "Senior IT Consultant / Business Analyst",
                "company": "Wilmar Consultancy Services",
                "location": "Medan, Indonesia",
                "time": "JULY 2018 – MAY 2022",
                "bullets": [
                    "Gathered and translated requirements into technical specifications",
                    "Optimized workflows reducing processing time under 3 minutes",
                    "Managed stakeholders across multi-region operations"
                ],
                "projects": [
                    "Built financial dashboards using real-time transaction data",
                    "Developed automated compliance reporting systems"
                ]
            },
            {
                "title": "Software Consultant Intern",
                "company": "Solita",
                "location": "Finland",
                "time": "APRIL 2023 – JUNE 2023",
                "bullets": [
                    "Captured requirements and converted into Agile user stories",
                    "Developed REST APIs for structured data exchange",
                    "Supported sprint planning and KPI tracking"
                ]
            }
        ],
        "projects": [
            {
                "title": "MineMatch Platform",
                "bullets": [
                    "Developed circular economy data-sharing platform",
                    "Enabled standardized exchange across stakeholders"
                ]
            }
        ],
        "tech": [
            {"title": "DATA", "value": "SQL, Python, Power BI"},
            {"title": "SYSTEMS", "value": "ERP, SAP, Logistics Platforms"}
        ],
        "skills": [
            {"title": "ANALYSIS", "value": "KPI, Optimization"},
            {"title": "BUSINESS", "value": "Stakeholder, Requirements"}
        ],
        "awards": [
            "Erasmus Mundus Scholarship",
            "Best Presenter Award"
        ],
        "education": {
            "focus": "Sustainability and Software Engineering",
            "thesis": "Automated ethical decision-support system"
        }
    }


# ------------------------
# SIMULATE COVER LETTER
# ------------------------
def simulate_cover_letter():
    return {
        "job_title": "Business Analyst",
        "company_name": "Euroclear Finland",
        "company_location": "Helsinki, Finland",
        "hiring_manager_name": "Hiring Manager",
        "company_address": "Helsinki Office",
        "letter_date": "March 2026",
        "body": [
            "I am applying for the Business Analyst position at Euroclear Finland. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc sed quam quis lorem bibendum ultricies. Proin magna lorem, dapibus et dui vitae, commodo bibendum nulla. Etiam molestie, sapien a tristique elementum, erat sapien semper tortor, eget porttitor ipsum ligula sed tellus. Vestibulum rutrum justo ut eros mattis varius. Morbi rhoncus, nisi eu cursus sodales, urna enim efficitur ligula, non aliquam libero urna a lectus. Fusce vulputate malesuada molestie.",
            "My experience aligns with requirements in financial systems and stakeholder coordination. Suspendisse vulputate consequat scelerisque. Praesent egestas molestie tortor vel euismod. Proin elementum velit eget enim pulvinar fringilla. Fusce ac ante ut dui volutpat tincidunt id vitae justo. Phasellus dapibus leo vitae tempus pharetra. Integer accumsan dolor est, eu porttitor dui elementum nec.",
            "I have delivered enterprise systems and optimized processes across global teams. Ut placerat volutpat turpis, ac aliquet dui finibus ut. Nullam ornare ut purus quis facilisis. Duis purus lectus, tincidunt ut justo id, malesuada malesuada tellus. Phasellus eleifend arcu mi, ac pharetra metus volutpat ornare. Integer accumsan ex quis ligula congue fringilla quis in neque. Quisque convallis rutrum arcu ut faucibus. Quisque libero diam, dapibus eu dui vitae, sodales vulputate sem. Etiam justo orci, mollis ac viverra at, blandit quis sem. Nunc eu quam diam.",
            "I am eager to contribute to your product development and innovation initiatives. Vivamus et vehicula justo. Phasellus volutpat justo in lobortis sodales. Etiam imperdiet euismod velit, sed molestie neque facilisis ac. Vivamus finibus, arcu sit amet euismod imperdiet, risus odio imperdiet tortor, non egestas ex magna a dui. Praesent accumsan dignissim quam, in cursus lorem. Etiam eu neque velit. Nunc ac faucibus lacus. Maecenas varius lacinia elementum. Nunc lacinia nunc at enim consectetur pulvinar."
        ]
    }