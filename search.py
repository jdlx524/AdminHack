'''
Function:
1. This file import ID,Tag,Title,Content,Picture,bert_keywords from final_result_w_bert.cvs
2. Calculate the bert_keywords with cmd input query to generate top 50 query content
Step1: Create corpus combining all keywords from all docs
Step2: Generate a tf-idf matrix for his corpus
Step3: Calculate query vector
Step4: Calculate each document vector
Step5: Calculate cosine similarity
Step6: Rank all docs by similarities in decending order

Usage:
python3 search.py filename.cvs "query content" topN
python3 search.py final_result_w_bert.csv "ticket season student" 50

Note:
This file should be under the same folder as final_result_w_bert.cvs
'''
import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# this is a function test file, final code in searchAPI.py

def main():
    filename = sys.argv[1]
    query = sys.argv[2].lower()
    topN = int(sys.argv[3])
    data = pd.read_csv(filename)
    #print(data.loc[3]['bert_keywords']) str type
    #Split by ,
    length = len(data['ID'])
    vocab = set()
    documents = []
    for i in range(length):
        keywords = data.loc[i]['bert_keywords'] #str
        try:
            # Since posts that has no content or invalid content
            # add tags to all the phrases
            phrases = [phrase.strip() for phrase in keywords.split(',')]
            phrases.remove('')
        except:
            phrases = [data.loc[i]['Tag']]
        documents.append(phrases)
    query = [query]
    # Preprocess your data by joining phrases with spaces
    documents_joined = [' '.join(doc) for doc in documents]
    query_joined = ' '.join(query)

    # Create a TfidfVectorizer object and fit it to your data
    vectorizer = TfidfVectorizer()
    vectorizer.fit(documents_joined + [query_joined])

    # Create a tf-idf matrix for the documents
    doc_tfidf_matrix = vectorizer.transform(documents_joined)

    # Create a tf-idf matrix for the query
    query_tfidf_matrix = vectorizer.transform([query_joined])
    similarity = cosine_similarity(doc_tfidf_matrix,query_tfidf_matrix)
    scores = {}
    for i in range(length):
        scores[i] = similarity[i][0]
    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    #print(scores)
    result_docID = []
    ranked_docID = [] # just get the top 50 for tag generation
    for i in range(topN):
        docID = scores[i][0] + 1 # real docID start from 1
        #docSimScore = scores[i][1] #not used
        result_docID.append(docID)
        if i < 50:
            ranked_docID.append(docID)
    print(result_docID)
    suggest_tag = getTag(data, ranked_docID)
    print(suggest_tag)
    
def getTag(data, ranked_docID):
    tags = {}
    for docID in ranked_docID:
        tag = data.loc[docID-1]["Tag"]
        if pd.isna(tag) or tag == "None":
            continue
        else:
            if tag in tags:
                tags[tag] += 1
            else:
                tags[tag] = 1
    ranked_tag = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    result = []
    for i in range(3):
        result.append(ranked_tag[i][0])
    return result
    
    
# this doesn't preserve the sequence of the tag, revise in SearchAPI file
# def getTag(data, ranked_docID):
#     tags = set()
#     for docID in ranked_docID:
#         tag = data.loc[docID-1]["Tag"]
#         if pd.isna(tag) or tag == "None":
#             continue
#         else:
#             tags.add(tag)
#             if len(tags) == 3:
#                 break
#     return tags

# def getTag(data, ranked_docID):
#     tags = []
#     for docID in ranked_docID:
#         tag = data.loc[docID-1]["Tag"]
#         if pd.isna(tag) or tag == "None":
#             continue
#         else:
#             if tag in tags:
#                 continue
#             else: tags.append(tag)
#             if len(tags) == 3:
#                 break
#     return tags
        


if __name__ == "__main__":
    main()
    # Define your documents and query as lists of phrases
    #document1 = ["the quick brown fox", "jumped over the lazy dog"]
    # document1 = ['388 semester need', '497 need graduate',
    #                         'class spring', 'class spring term',
    #                         'day scholarships come', 'department tuition fee',
    #                         'ece fall 2023', 'eecs 388 semester',
    #                         'fall 2023 questions', 'going graduating year',
    #                         'gym palmer', 'intern international student',
    #                         'international student help']
    # document2 = ['machine temporary gym', 'need graduate ulcs',
    #                         'palmer field gym', 'plans town week',
    #                         'recently admitted student',
    #                         'scholarships come specifically',
    #                         'set day scholarships', 'spring term midterm',
    #                         'student ross dream', 'taking class spring',
    #                         'temporary gym', 'temporary gym palmer']
    # documents = [document1, document2]
    # query = ["international student"]

    # # Preprocess your data by joining phrases with spaces
    # documents_joined = [' '.join(doc) for doc in documents]
    # query_joined = ' '.join(query)

    # # Create a TfidfVectorizer object and fit it to your data
    # vectorizer = TfidfVectorizer()
    # vectorizer.fit(documents_joined + [query_joined])

    # # Create a tf-idf matrix for the documents
    # doc_tfidf_matrix = vectorizer.transform(documents_joined)

    # # Create a tf-idf matrix for the query
    # query_tfidf_matrix = vectorizer.transform([query_joined])

    # # Print the tf-idf matrices
    # print("Document TF-IDF matrix:")
    # print(doc_tfidf_matrix.toarray())
    # print()
    # print("Query TF-IDF matrix:")
    # print(query_tfidf_matrix.toarray())
    # similarity = cosine_similarity(doc_tfidf_matrix,query_tfidf_matrix)
    # print(similarity)