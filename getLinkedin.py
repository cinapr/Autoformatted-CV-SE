import os
import sys
import json
import pyperclip

from Controllers.Utilities.schema import (
    validate_json,
    CV_SCHEMA,
    COVERLETTER_SCHEMA,
    CHECK_SCHEMA
)
from Controllers.Utilities.gpt_call import generate_json
from Controllers.Utilities.get_linkedin import scrape_job_description, scrape_job_description_manual
from Controllers.Utilities.utility import load_file, save_text
from Controllers.fix_cv_schema import fix_cv_schema
from Controllers.generate_docx_cv import generate_docx_cv
from Controllers.generate_docx_coverletter import generate_docx_coverletter
from Controllers.Utilities.mock_gpt import (
    simulate_check,
    simulate_cv,
    simulate_cover_letter,
    manual_gpt
)


# ------------------------
# MAIN
# ------------------------
def main():
    while (True):
        #IF SOME PARAMETER NOT PASSED
        url = input("URL: ") or ""
        if ((url == "") or (url == "EXIT") or (url == "exit") or (url.capitalize == "Q") or (url.capitalize == "Z")):
            return
        
        job_desc = scrape_job_description(url)

        print(job_desc + "\n\n\n")



if __name__ == "__main__":
    main()