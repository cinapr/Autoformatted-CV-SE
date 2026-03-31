import json

def simulate_gpt():
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
                # no projects → test optional logic
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