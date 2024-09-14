import sys
import time
from gallery import download, gallery_manage

file_name = sys.argv[1]  # storage path
link_file = sys.argv[2]  # link file path
with open(link_file, 'r') as file:
    links = file.readlines()
links = [link.strip() for link in links]
for line in links:
    # gfycat is ignored, it provides gif
    all_set = line.split()
    if len(all_set) == 1:
        continue
    ID = int(all_set[0])
    link_set = all_set[1:]
    idx = 1
    for link in link_set:
        print(link)
        if 'i.imgur.com' in link or 'i.redd.it' in link or 'redgifs.com' in link or "preview.redd.it" in link:
            download(ID, link, str(idx), file_name)
            idx += 1
            time.sleep(0.5)
        elif 'www.reddit.com/gallery/' in link:
            gallery_name = ''
            for i in range(len(link)-1, 0, -1):
                if link[i] == '/':
                    gallery_name = link[i+1:]
                    break
            url_g = 'https://www.reddit.com/comments/' + gallery_name + '.json'
            idx = gallery_manage(ID, url_g, file_name, idx)
            time.sleep(0.5)
