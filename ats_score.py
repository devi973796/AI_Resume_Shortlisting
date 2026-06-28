def calculate_ats(text, skills):
    score = 0

    text = text.lower()

    for skill in skills:
        if skill.lower() in text:
            score += 1   # always number

    return float(score * 10)