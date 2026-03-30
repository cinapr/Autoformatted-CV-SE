import requests
from bs4 import BeautifulSoup

def scrape_job_description(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # Try common containers
    desc = soup.get_text(separator="\n")

    return desc[:8000]  # limit size for GPT

#print (scrape_job_description("https://www.linkedin.com/jobs/view/4365130519/"))