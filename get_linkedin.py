import requests
from bs4 import BeautifulSoup

def clean_text(text):
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        line = line.strip()
        if len(line) < 2:
            continue
        if "sign in" in line.lower():
            continue
        if "join now" in line.lower():
            continue
        if "linkedin" in line.lower():
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


def scrape_job_description(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # -------------------------
    # TITLE
    # -------------------------
    title = soup.find("h1")
    job_title = title.get_text(strip=True) if title else "N/A"

    # -------------------------
    # COMPANY
    # -------------------------
    company = soup.find("a", {"class": "topcard__org-name-link"})
    company_name = company.get_text(strip=True) if company else "N/A"

    # -------------------------
    # LOCATION
    # -------------------------
    location = soup.find("span", {"class": "topcard__flavor--bullet"})
    location_text = location.get_text(strip=True) if location else "N/A"

    # -------------------------
    # DESCRIPTION
    # -------------------------
    desc = soup.find("div", {"class": "description__text"})
    
    if desc:
        job_desc = clean_text(desc.get_text(separator="\n"))
    else:
        # fallback (if class not found)
        job_desc = clean_text(soup.get_text(separator="\n"))

    # limit size for GPT
    job_desc = job_desc[:5000]

    # -------------------------
    # FINAL FORMAT
    # -------------------------
    result = f"""COMPANY NAME: {company_name}
JOB TITLE: {job_title}
LOCATION: {location_text}

JOB ADS:
{job_desc}
"""

    return result


# test
if __name__ == "__main__":
    url = "https://www.linkedin.com/jobs/view/4365130519/"
    print(scrape_job_description(url))