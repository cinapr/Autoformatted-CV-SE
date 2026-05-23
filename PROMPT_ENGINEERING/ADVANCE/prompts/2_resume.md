Based on the job description you just analyzed, generate a tailored CV.
- Keep bullets tight (80-100 characters). Match duties with quantifiable outcomes using my existing data.
- Merge the Wilmar research into the SDLC position if the job isn't research-focused.
- Budget: Exactly 1 A4 page (max 40 lines, 500-570 words). Dedicate the most volume to the recent Wilmar role.
- Do not generate placeholder text.

Output strictly in this JSON schema:
{
  "summary": ["string"],
  "tech": [{"label": "string", "value": "string"}],
  "skills": [{"label": "string", "value": "string"}],
  "experience": [
    {
      "title": "string",
      "company": "string",
      "location": "string",
      "time": "string",
      "bullets": ["string"],
      "projects": ["string"]
    }
  ],
  "projects": [
    {
      "title": "string",
      "bullets": ["string"]
    }
  ],
  "education": {
    "focus": "string",
    "thesis": "string"
  },
  "awards": ["string"]
}