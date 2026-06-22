def calculate_ats(match, skills):

    score = 0


    # Resume similarity
    score += match * 0.6


    # Skills
    score += len(skills) * 5


    if score > 100:

        score = 100


    return round(score,2)