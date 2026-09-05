# AI Job Matcher

A Django-based web application that fetches live job listings from LinkedIn and uses Google's Gemini AI to analyze, score, and match candidate resumes against job descriptions in real-time.

---

## Features

* **Resume Parsing:** Upload a PDF resume to extract and store candidate technical skills during the session.
* **Live LinkedIn Job Fetching:** Scrapes public job listings dynamically based on query and location without requiring API keys for scraping.
* **AI Match & Categorization:** Evaluates job listings using Google's Gemini AI and categorizes them into match percentage tiers (90-100%, 70-89%, 50-69%, and Filtered).
* **Detailed Match Breakdown:** Highlights matched skills, missing skills, and provides an AI-generated summary for each job posting.
* **Saved Jobs:** Bookmark interesting roles locally to review or apply later.
* **Responsive Dark Dashboard:** Built with Bootstrap 5 for a clean, modern interface.

---

## Tech Stack

* **Backend:** Python, Django
* **AI Model:** Google Gemini API (`gemini-3.5-flash-lite` via `google-genai`)
* **Scraping / Scraping Parser:** `requests`, `beautifulsoup4`
* **Resume Processing:** `pypdf`
* **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/palapeshmarga/JobFinder.git
cd JobFinder
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install django google-genai requests beautifulsoup4 pypdf
```

### 4. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/`.

---
---
<h2>Usage</h2> 
<strong>
<ol start="1" data-path-to-node="12">
  <li>
    <p data-path-to-node="12,0,0">Click <b data-path-to-node="12,0,0" data-index-in-node="6">API Settings</b> in the top navigation bar and enter your <b data-path-to-node="12,0,0" data-index-in-node="60">Gemini API Key</b>.</p>
  </li>
  <li>
    <p data-path-to-node="12,1,0">Upload your PDF resume.</p>
  </li>
  <li>
    <p data-path-to-node="12,2,0">Enter a target job title (e.g., <code data-path-to-node="12,2,0" data-index-in-node="32">Python Developer</code>) and location (e.g., <code data-path-to-node="12,2,0" data-index-in-node="70">Remote</code>).</p>
  </li>
  <li>
    <p data-path-to-node="12,3,0">Click <b data-path-to-node="12,3,0" data-index-in-node="6">Search &amp; Analyze Jobs</b> to view categorized match results.</p>
  </li>
</ol>