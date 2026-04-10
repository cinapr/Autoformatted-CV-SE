import os
import sys
import json
import pyperclip

from Controllers.Utilities.get_linkedin import scrape_job_description, scrape_job_description_manual

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