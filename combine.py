import csv
import sys

text_file = sys.argv[1]
pic_file = sys.argv[2]
# text_file = "all_crawl/new_text.csv"
# pic_file = "new_ocr.csv"
# query_file = "test_data/200 query.txt"
with open(text_file, newline='') as csvfile, open(pic_file, newline='') as picfile, open("new_final_result.csv", 'w', newline='') as writefile:
    reader1 = csv.reader(csvfile)
    reader2 = csv.reader(picfile)
    writer = csv.writer(writefile)
    next(reader1)
    next(reader2)
    writer.writerow(['ID', 'Tag', 'Title', 'Content', 'Picture'])
    pic_dic = {}
    for row in reader2:
        ID, pic_content = row[0], row[1]
        pic_dic[ID] = pic_content
    for row in reader1:
        ID, tag, title, content = row[0], row[1], row[2], row[3]
        writer.writerow([ID, tag, title, content, pic_dic.get(ID, '')])
