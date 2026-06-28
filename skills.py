skills_list = [

"python",
"java",
"sql",
"machine learning",
"deep learning",
"angular",
"react",
"flask",
"django",
"aws",
"docker",
"html",
"css",
"javascript",
"mongodb"

]


def find_skills(text):
    skills_list = ["python", "java", "sql", "flask", "html", "css"]

    found = []

    text = text.lower()

    for skill in skills_list:
        if skill in text:
            found.append(skill)

    return found   # 👈 MUST BE LIST