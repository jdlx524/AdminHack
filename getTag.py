"""retrieveTag4GroundTruth"""
import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# this is a function test file, final code in searchAPI.py

def getTagPerFile(query, topN, data):
    topN = int(topN)
    length = len(data['ID'])
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
    suggest_tag = getTag(data, result_docID)
    return suggest_tag

def getTag(data, ranked_docID):
    tags = set()
    for docID in ranked_docID:
        tag = data.loc[docID-1]["Tag"]
        if pd.isna(tag) or tag == "None":
            continue
        else:
            tags.add(tag)
            if len(tags) == 3:
                break
    return tags

def retrieveTag4GroundTruth(filename = "final_result_w_bert.csv"):
    data = pd.read_csv(filename)
    length = len(data)
    result = {}
    for i in range(length):
        query = data.loc[i]['bert_keywords']
        query = query.replace(",", "")
        tags = getTagPerFile(query, 50 ,data)
        result[i] = list(tags)
    return result

retrieveTag4GroundTruth()
        
