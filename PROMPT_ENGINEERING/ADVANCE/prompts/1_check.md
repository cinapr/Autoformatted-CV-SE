Evaluate this job description against my profile. Be strict, realistic, and practical. 
If there are major blockers (like missing a mandatory PhD, specific tech stack, or language), mark suitability as false.

Here is the Job Description:
{{JOB_DESCRIPTION}}

Output strictly in this JSON schema:
{
  "match_score": 0,
  "is_suitable": true,
  "visa_sponsorship": "NO SPONSORSHIP EXPLICITLY | NO TALK ABOUT SPONSORSHIP | SPONSORSHIP/RELOCATION IS CONSIDERED | SPONSORSHIP IS GIVEN",
  "language_fit": "string (comma separated list of required languages)",
  "missing_requirements": ["string"],
  "mandatory_documents": ["string"],
  "cover_letter_required": true,
  "additional_answers": [{"question": "string", "answer": "string"}]
}