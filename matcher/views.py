from django.shortcuts import render
from .job_fetcher import fetch_linkedin_jobs, JobFetchError
from .ai_matcher import process_and_categorize_jobs
import pypdf # or pdfplumber / PyPDF2 depending on your resume extractor logic


def index(request):
    context = {
        "current_query": "",
        "current_location": "Remote",
        "current_page": 1,
        "has_resume": False,
        "categorized_results": None,
        "error_message": None,
    }

    # Check if resume text exists in session
    resume_text = request.session.get("resume_text", "")
    if resume_text:
        context["has_resume"] = True

    if request.method == "POST":
        gemini_key = request.POST.get("gemini_key", "").strip()
        search_query = request.POST.get("search_query", "").strip()
        location = request.POST.get("location", "Remote").strip()
        page = int(request.POST.get("page", 1))

        context["current_query"] = search_query
        context["current_location"] = location
        context["current_page"] = page

        # 1. Check Gemini Key
        if not gemini_key:
            context["error_message"] = "Gemini API Key is missing! Click 'API Settings' to save it."
            return render(request, "/home/pala-peshmarga/Desktop/JobFinder/matcher/templates/matcher/index.html", context)

        # 2. Process Resume File if uploaded
        if "resume" in request.FILES:
            file = request.FILES["resume"]
            try:
                # Basic PyPDF text extraction
                reader = pypdf.PdfReader(file)
                extracted_text = ""
                for page_obj in reader.pages:
                    extracted_text += page_obj.extract_text() or ""
                
                request.session["resume_text"] = extracted_text
                resume_text = extracted_text
                context["has_resume"] = True
            except Exception as e:
                context["error_message"] = f"Failed to process resume PDF: {e}"
                return render(request, "/home/pala-peshmarga/Desktop/JobFinder/matcher/templates/matcher/index.html", context)

        if not resume_text:
            context["error_message"] = "Please upload a PDF resume to analyze jobs."
            return render(request, "/home/pala-peshmarga/Desktop/JobFinder/matcher/templates/matcher/index.html", context)

        # 3. Fetch jobs using LinkedIn Guest scraper
        try:
            jobs = fetch_linkedin_jobs(query=search_query, location=location, page=page)
        except JobFetchError as e:
            context["error_message"] = str(e)
            return render(request, "/home/pala-peshmarga/Desktop/JobFinder/matcher/templates/matcher/index.html", context)

        # 4. Categorize jobs with Gemini AI
        categorized = process_and_categorize_jobs(
            resume_text=resume_text,
            jobs=jobs,
            provider="gemini",
            api_key=gemini_key
        )

        context["categorized_results"] = categorized

    return render(request, "/home/pala-peshmarga/Desktop/JobFinder/matcher/templates/matcher/index.html", context)