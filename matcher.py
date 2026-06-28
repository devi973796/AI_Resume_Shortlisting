def calculate_match(resume_text, job_text):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    match = len(resume_words & job_words)

    return float(match)   # 👈 IMPORTANT