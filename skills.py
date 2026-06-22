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

    text=text.lower()


    found=[]


    for skill in skills_list:

        if skill in text:

            found.append(skill)


    return found