import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def retrieve(searchTerm, filename, topN=50):
    query = searchTerm.lower()
    data = pd.read_csv(filename)
    length = len(data['ID'])
    topN = int(topN)
    documents = []
    for i in range(length):
        keywords = data.loc[i]['bert_keywords_top1'] #str
        try:
            # Since posts that has no content or invalid content
            # add tags to all the phrases
            phrases = [phrase.strip() for phrase in keywords.split(',')]
            phrases.remove('')
        except:
            phrases = [data.loc[i]['Tag']]
        documents.append(phrases)
    query = [query]
    print("query=", query)
    # Preprocess your data by joining phrases with spaces
    # print(documents[0])
    documents_joined = [' '.join([str(word) for word in doc]) for doc in documents]
    # documents_joined = []
    # for doc in documents:
    #     for word in doc:
    #         print(word)
    #         documents_joined.append(word+' ')
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
    rankedID = {}
    top30 = []
    for i in range(30):
        docID = scores[i][0] + 1
        top30.append(docID)
    for i in range(topN):
        docID = scores[i][0] + 1 # real docID start from 1
        #ID,Tag,Title,Content,Picture,bert_keywords
        docInfo = data.loc[docID-1]
        
        # tagVal = "" if np.isnan(docInfo['Tag']) else docInfo['Tag']
        # titleVal = "" if np.isnan(docInfo['Title']) else docInfo['Title']
        # contentVal = "" if np.isnan(docInfo['Content']) else docInfo['Content']
        # result[docID] = {
        #     "Tag" :  tagVal,
        #     "Title" : titleVal,
        #     "Content" : contentVal
        # }
        rankedID[i] = {
            "ID" : docID,
            "Tag" :  docInfo['Tag'],
            "Title" : docInfo['Title'],
            "Content" : docInfo['Content']
        }
    suggested_tags = getTag(data, top30)
    result = {
        "posts" : rankedID,
        "suggestedTags" : list(suggested_tags)
    }
    return result

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