# Reddit Post Collector and Analyzer

![Project Overview](./output.gif) 

## Overview:
For our hackathon project, we developed a comprehensive Reddit post collection and analysis tool. The system leverages the Reddit and Pushshift APIs to gather a large dataset of Reddit posts. We successfully collected **34,137 posts** and processed them for further analysis.

## Inspiration:
Existing tools for scraping and analyzing Reddit data often miss the valuable information hidden within images, such as memes, screenshots, and image posts. With the overwhelming amount of information available, users often get tired of manually searching for insights. We wanted to create a solution that not only retrieves textual data but also extracts meaning from images using OCR (Optical Character Recognition), providing a more holistic view of user activity and trends.

## Technical Difficulty:
We faced several **real technical challenges**, such as overcoming Reddit API limitations (which allow a maximum of 1000 posts) and efficiently processing large datasets. By using the Pushshift API, we gathered **34,137 posts** and applied advanced image processing techniques to ensure both text and images were analyzed effectively.

## Usefulness:
Our system's search capabilities allow users to retrieve relevant posts or data based on both text and OCR-extracted keywords from images. This can be used in various fields like **research**, **marketing**, and **content analysis**. The flexibility of our system also allows it to be adapted to other websites, making it a scalable solution.

## Technical Stack:
We used the following tools and technologies to build this project:
- **Python** for core logic and processing.
- **HTML** for web integration.
- **Reddit API** and **Pushshift API** for data collection.
- **OCR (Tesseract)** for text extraction from images.
- **BERT** and **TextRank** for keyword extraction.
- **Hugging Face Transformers** for NLP-based processing.
- **React** for frontend development.
- **Flask** for backend API integration.

---

## Key Features:

### 1. Post Collection:
We retrieve the literal content of posts (titles, tags, text, and images) for analysis and store this data in a structured table (CSV format). For image-based posts, especially those under "www.reddit.com/gallery/", we use the Reddit API to extract individual image URLs.

### 2. Image Download and OCR:
Using the URLs, we download images and apply Optical Character Recognition (OCR) to extract textual information from them. The extracted text is stored alongside the respective post information in a unified table (CSV) for further analysis.

### 3. Search Functionality:
We integrated the Reddit search API to retrieve a user-specified number of top search results for specific queries. This allows flexible search options for users to query specific topics or trends.

### 4. Keyword Extraction:
We applied advanced keyword extraction methods using **BERT** and **TextRank** to identify relevant keywords from both the post content and OCR data. The results are stored in the final dataset and used to enhance search and retrieval performance.

### 5. Data Combination:
The system combines textual content and OCR data into a single CSV file for comprehensive analysis, ensuring both post content and image-derived text are searchable.

### 6. Evaluation and Search API:
Our system evaluates the precision and recall for retrieving relevant posts and suggests post tags based on keyword similarity and ground truth data. The Search API ranks posts based on query similarity using **TF-IDF** and **cosine similarity** techniques.

---

## Final Output:
All the collected and processed information is stored in a final CSV file (`final_result.csv`), which is then enhanced with keyword extraction results in `final_result_w_bert.csv`.

---

This project enables efficient data collection and analysis of both textual and visual content from Reddit, offering keyword-based search and retrieval capabilities. It is a flexible, scalable solution that can easily be adapted to other websites or platforms generating user content.

## Function Usage

### all_crawler
```bash
python3 all_crawler.py
```
This file is used to obtain the contents of the top totalResults posts under the general sorting. The text results are located in "../all_crawl/text.csv", and the link results are located in "../all_crawl/links".
### download_pic
```bash
python3 download_pic.py [storage path] [link file path]
```
Download pictures to AllCrawl.  
The first argument gives where you want to store pictures. The second one gives where to find download links.
### OCR
```bash
python3 ocr.py [picture folder path]
```
Extract textual information from pictures.  
The first arguement is the path of folder containing all crawled pictures. The folder is recommended to be in the same folder as the program. In this folder, pictures should be placed in subfolders named after their corresponding postids. The output is a csv file with columns of postid and ocr_text.
### combine
```bash
python3 combine.py [text csv file] [ocr_text csv file]
```
Combine csv file gotten by crawler and csv file gotten by OCR.  
The first arguement is the csv file gotten by crawler, and the second argument is the csv file gotten by OCR. The output is a combined csv file.
### search_result
```bash
python3 search_result.py [text_file] [query_file] [search_result_file] [new_text_file] [new_link_file]
```
Get search result for queries.  
meaning of arguments: text file containing 10000 posts, query file containing search queries, storage place for search result, storage place for newly added posts' text, storage place for newly added posts' link.
### file position
All information is integrated into final_result.csv, processed and stored in final_result_w_bert.csv, and the test data used for evaluation is located in test_data/.
## Keyword extraction
### bert.py 
```bash
python3 bert.py [min_n_gram] [max_n_gram]
```

### text_rank.py
```bash
python3 text_rank.py
```

Results will be stored in final_result_w_bert_new.csv. Make sure having huggingface packages (transformer, sentence_transformer) installed.

Print out Retreived doc ID
