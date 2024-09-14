import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from itertools import tee, zip_longest
from datasets import load_dataset
# nltk.download('stopwords', download_dir='/nfs/turbo/coe-ahowens/zxp/Anaconda3/envs/MAE/nltk_data')
import pandas as pd

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

def get_keywords(text, n):

    sentences = sent_tokenize(text)
    words = []
    for sentence in sentences:
        words += word_tokenize(sentence)
    
    # filter out stopwords and punctuations
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.lower() not in stop_words]
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(' '.join(words))
    
    # perform stemming on the words
    # porter = PorterStemmer()
    # stemmed_words = [porter.stem(word) for word in words]
    
    stemmed_words = words
    
    # Calculate the term frequency of each word
    freq_dist = FreqDist(stemmed_words)
    
    # create a graph with words as nodes and co-occurring words as edges
    graph = {}
    for i, word1 in enumerate(stemmed_words):
        if word1 not in graph:
            graph[word1] = {}
        for j, word2 in enumerate(stemmed_words):
            if i != j:
                if word2 not in graph[word1]:
                    graph[word1][word2] = 1
                else:
                    graph[word1][word2] += 1
    
    # Calculate the PageRank score of each word, with damping factor 0.85, initial score 1.0
    damping_factor = 0.85
    max_iterations = 100
    scores = {}
    for word in graph:
        scores[word] = 1.0
    for i in range(max_iterations):
        for word1 in graph:
            score = 1 - damping_factor
            for word2 in graph[word1]:
                score += damping_factor * graph[word1][word2] / freq_dist[word2]
            scores[word1] = score
    
    # return top n words
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [word for word, score in sorted_scores][:n]
    return top_keywords

    
data_files = {"train": "final_result.csv"}
train_data = load_dataset("csv", data_files="final_result.csv")

result = []

for i in range(len(train_data["train"]["Content"])):
    print(i)
    text = ""
    if train_data["train"]["Title"][i]:
        text += train_data["train"]["Title"][i] + ' '
    if train_data["train"]["Content"][i]:
        text += train_data["train"]["Content"][i] + ' '
    if train_data["train"]["Picture"][i]:
        text += train_data["train"]["Picture"][i]
    
    cands = ""
    
    try:
        key_phrases = get_keywords(text, 5)
    except:
        result.append("")
        continue
    
    for p in key_phrases:
        cands += p + ", "
        print(i)
    print(cands)
    
    result.append(cands)


df = pd.read_csv('final_result_w_text_rank.csv')
new_column = pd.DataFrame({'text_rank_keywords': result})
df = df.merge(new_column, left_index = True, right_index = True)
df.to_csv('final_result_w_text_rank.csv', index = False)