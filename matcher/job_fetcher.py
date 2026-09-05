import requests
from bs4 import BeautifulSoup


class JobFetchError(Exception):
    """A safe error that can be displayed to the user."""


def clean_html(raw_html):
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ").strip()


def fetch_linkedin_jobs(query=None, location=None, page=1, **kwargs):
    search_query = query if query else "Software Developer"
    search_location = location if location else "Remote"

    start = (int(page) - 1) * 25
    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    params = {
        "keywords": search_query,
        "location": search_location,
        "start": start
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 429:
            raise JobFetchError("LinkedIn is rate-limiting requests right now. Try again in a minute.")
        elif response.status_code != 200:
            raise JobFetchError(f"LinkedIn returned status code {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.select("li")

        if not job_cards:
            raise JobFetchError(f"No LinkedIn jobs found for '{search_query}'.")

        formatted_jobs = []
        for index, card in enumerate(job_cards[:8]):
            title_el = card.select_one("h3.base-search-card__title")
            company_el = card.select_one("h4.base-search-card__subtitle")
            location_el = card.select_one("span.job-search-card__location")
            date_el = card.select_one("time")
            link_el = card.select_one("a.base-card__full-link")

            title = title_el.get_text(strip=True) if title_el else search_query
            company = company_el.get_text(strip=True) if company_el else "Tech Company"
            job_loc = location_el.get_text(strip=True) if location_el else search_location
            date_posted = date_el.get_text(strip=True) if date_el else "Recently"
            apply_link = link_el["href"] if link_el and link_el.has_attr("href") else "https://www.linkedin.com/jobs"

            formatted_jobs.append({
                "job_id": f"guest_{page}_{index}",
                "title": title,
                "company": company,
                "location": job_loc,
                "date_posted": date_posted,
                "apply_link": apply_link,
                "description": f"{title} position at {company} in {job_loc}."
            })

        return formatted_jobs

    except Exception as error:
        if isinstance(error, JobFetchError):
            raise error
        raise JobFetchError(f"Failed to scrape LinkedIn jobs: {error}")