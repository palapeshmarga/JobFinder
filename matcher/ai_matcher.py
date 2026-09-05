import json
import time
from google import genai
from google.genai import types


def process_and_categorize_jobs(resume_text, jobs, provider="gemini", api_key=None):
    if not jobs or not api_key:
        return {}

    client = genai.Client(api_key=api_key)
    formatted_jobs = [
        {
            "index": index,
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "description": job.get("description"),
        }
        for index, job in enumerate(jobs)
    ]

    prompt = f"""
    You are an expert technical recruiter analyzing candidate eligibility for software engineering roles.
    
    CRITICAL SCORING RULES:
    1. Base the `match_score` strictly on skill overlap.
    2. If the job requires core skills present in the resume (e.g., Python, Django, JavaScript, React, REST APIs), start from a base score of 70%+.
    3. NEVER return 0% if the candidate possesses primary skills mentioned in the job post (like Python). A role matching any core tech stack requirement must score at least 30-50% minimum.
    4. Provide an accurate list of `matched_skills` (skills present in BOTH resume and job description) and `missing_skills` (required job skills missing from resume).

    CANDIDATE RESUME:
    {resume_text[:8000]}

    JOB LISTINGS:
    {json.dumps(formatted_jobs, indent=2)}

    For EACH job index, return a JSON array of objects with keys:
    - "index": int
    - "match_score": int (0-100)
    - "summary": string (2 sentences max explaining the score justification)
    - "matched_skills": list of strings
    - "missing_skills": list of strings

    Return ONLY a valid JSON array.
    """

    response = None
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
            )
            break
        except Exception as error:
            if ("429" in str(error) or "503" in str(error)) and attempt < max_retries - 1:
                time.sleep(3)
                continue
            if attempt == max_retries - 1:
                print(f"Error calling Gemini API after retries: {error}")
                return {
                    "90-100%": [],
                    "70-89%": [],
                    "50-69%": [],
                    "Filtered": [
                        {
                            **job,
                            "match_score": 0,
                            "date_posted": job.get("date_posted", "Recently"),
                            "summary": f"API Error: {error}",
                            "matched_skills": [],
                            "missing_skills": [],
                        }
                        for job in jobs
                    ],
                }

    try:
        evaluations = json.loads(response.text)
        eval_map = {
            item["index"]: item for item in evaluations if "index" in item
        }
        categorized = {
            "90-100%": [],
            "70-89%": [],
            "50-69%": [],
            "Filtered": [],
        }

        for index, job in enumerate(jobs):
            evaluation = eval_map.get(index, {})
            score = evaluation.get("match_score", 0)
            job_data = {
                **job,
                "match_score": score,
                "date_posted": job.get("date_posted", "Recently"),
                "summary": evaluation.get(
                    "summary", "No evaluation available."
                ),
                "matched_skills": evaluation.get("matched_skills", []),
                "missing_skills": evaluation.get("missing_skills", []),
            }

            if score >= 90:
                categorized["90-100%"].append(job_data)
            elif score >= 70:
                categorized["70-89%"].append(job_data)
            elif score >= 50:
                categorized["50-69%"].append(job_data)
            else:
                categorized["Filtered"].append(job_data)

        return categorized
    except Exception as error:
        print(f"Error parsing AI JSON response: {error}")
        return {
            "90-100%": [],
            "70-89%": [],
            "50-69%": [],
            "Filtered": [
                {
                    **job,
                    "match_score": 0,
                    "date_posted": job.get("date_posted", "Recently"),
                    "summary": f"Parsing Error: {error}",
                    "matched_skills": [],
                    "missing_skills": [],
                }
                for job in jobs
            ],
        }