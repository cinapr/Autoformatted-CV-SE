Automated Tailored CV Generator Pipeline
========================================

This project is a lightweight, AI-driven pipeline that automatically evaluates job descriptions and generates highly tailored Resumes and Cover Letters.

Instead of hardcoding complex AI prompts into Python strings, this project uses **Externalized Prompt Engineering**. All AI instructions, schemas, and context data are kept in clean Markdown (`.md`) and Text (`.txt`) files. The Python script simply acts as an engine to pass these files to the Gemini API while maintaining a persistent context window.

Features
--------

-   **Context Preservation:** Uses Gemini's `start_chat()` session to remember your master profile across multiple generation steps, reducing API token waste.

-   **Externalized Prompts:** Edit the AI's behavior, rules, and JSON schemas directly in Markdown files without touching a single line of Python.

-   **Smart Suitability Check:** Automatically halts the pipeline if the job description contains critical blockers (e.g., missing mandatory languages or no visa sponsorship).

-   **Strict JSON Outputs:** Forces the AI to return clean JSON data, making it incredibly easy to plug the output into Word Document (`.docx`) or LaTeX template generators later.

Project Structure
-----------------

Plaintext

```
cv_pipeline/
│
├── context/
│   ├── system_instruction.md  # The AI's master persona and strict rules
│   └── cindy_profile.txt      # Your master career history and projects
│
├── prompts/
│   ├── 1_check.md             # Analyzes job fit and extracts keywords
│   ├── 2_resume.md            # Generates the tailored CV JSON
│   └── 3_coverletter.md       # Generates the tailored Cover Letter JSON
│
├── automate_v2.py             # The main Python execution engine
└── README.md                  # This file

```

Prerequisites
-------------

You need Python installed on your system and the Google Generative AI SDK.

1.  Install the required Python library:

    Bash

    ```
    pip install google-generativeai

    ```

2.  Get a free Gemini API key from Google AI Studio.

3.  Set your API key as an environment variable so the script can access it securely:

    **Mac/Linux:**

    Bash

    ```
    export GEMINI_API_KEY="your_api_key_here"

    ```

    **Windows (Command Prompt):**

    DOS

    ```
    set GEMINI_API_KEY=your_api_key_here

    ```

    **Windows (PowerShell):**

    PowerShell

    ```
    $env:GEMINI_API_KEY="your_api_key_here"

    ```

Setup & Usage
-------------

1.  **Update your profile:** Open `context/cindy_profile.txt` and paste your complete, untailored master resume and project history.

2.  **Review the Persona:** Check `context/system_instruction.md` to ensure the AI's boundaries and rules match your preferences.

3.  **Run the script:**

    Bash

    ```
    python automate_v2.py

    ```

4.  **Follow the prompt:** The terminal will ask you to paste the Job Description you want to apply for. Press Enter to submit.

The script will run through the three phases. If the job is a suitable match, it will output two files into your root directory:

-   `data_cv.json`

-   `data_cl.json`

Customization
-------------

The beauty of this architecture is how easily it can be modified.

-   **Want a different Cover Letter tone?** Just edit `prompts/3_coverletter.md`.

-   **Need a different JSON schema for a new Word template?** Update the JSON block inside `prompts/2_resume.md`. The Python code requires zero changes.