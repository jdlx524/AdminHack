import numpy as np
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import load_dataset
import sys

from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity

import os

# os.environ['SENTENCE_TRANSFORMERS_HOME'] = '/scratch/ahowens_root/ahowens1/zxp/.cache/'
test_file = "new_final_result.csv"
data_files = {"train": test_file}
train_data = load_dataset("csv", data_files=test_file)

nGramRange = (int(sys.argv[1]), int(sys.argv[2]))

stop_words = "english"

model = SentenceTransformer('distilbert-base-nli-mean-tokens')

result = []

for i in range(len(train_data["train"]["Content"])):
    text = ""
    if train_data["train"]["Title"][i]:
        text += train_data["train"]["Title"][i] + ' '
    if train_data["train"]["Content"][i]:
        text += train_data["train"]["Content"][i] + ' '
    if train_data["train"]["Picture"][i]:
        text += train_data["train"]["Picture"][i]

    # extract candidate keywords and/or phrases from 'text'
    try:
        count = CountVectorizer(ngram_range=nGramRange, stop_words=stop_words).fit([text])
    except Exception as e:
        result.append("")
        print(e)
        continue
    # count = CountVectorizer(ngram_range=nGramRange, stop_words=stop_words).fit([text])

    candidates = count.get_feature_names_out()

    # print(candidates)

    # Get feature of whole document
    doc_embedding = model.encode([text])

    # feature of candidate phrases
    candidate_embeddings = model.encode(candidates)

    distances = cosine_similarity(doc_embedding, candidate_embeddings)

    top_n = 5
    keyphrases = [candidates[index] for index in distances.argsort()[0][-top_n:]]

    cands = ""

    for p in keyphrases:
        cands += p + ", "
    if not (i%100):
        print(cands)

    result.append(cands)

df = pd.read_csv(test_file)
new_column = pd.DataFrame({'bert_keywords_top1': result})
df = df.merge(new_column, left_index=True, right_index=True)
df.to_csv('final_result_w_bert_cs.csv', index=False)
