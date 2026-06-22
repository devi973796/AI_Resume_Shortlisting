from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity



def calculate_match(resume, job):


    data = [resume, job]


    vectorizer = TfidfVectorizer()


    vectors = vectorizer.fit_transform(data)


    score = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]


    percentage = round(
        score*100,
        2
    )


    return percentage