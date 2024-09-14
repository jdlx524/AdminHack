import os
import sys
from PIL import Image
import numpy as np
import pytesseract
import csv


# Windows user need to add the path of executable
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def main():
    """Do OCR. Accept the folder name as argument."""
    if len(sys.argv) < 2:
        print("Missing arguments!")
        sys.exit(1)
    path = os.getcwd()+"/"+sys.argv[1]
    subfolders = [os.path.join(path, name) for name in os.listdir(
        path) if os.path.isdir(os.path.join(path, name))]
    with open(os.getcwd()+"/"+"ocr.csv", 'a', newline='') as fptr:
        writer = csv.writer(fptr)
        writer.writerow(["Num", "OCR_text"])
        idx=0
        for subfolder in subfolders:
            ocr_text = []
            idx += 1
            if idx<1324: continue
            if idx%10==0: print(subfolder)
            for file in os.listdir(subfolder):
                if file.endswith((".png", ".jpg", ".jpeg")):
                    try:
                        img = Image.open(os.path.join(subfolder, file))
                        # print(os.path.join(subfolder, file))
                    except:
                        continue
                    text = pytesseract.image_to_string(img, lang="eng")
                    # print(text)
                    ocr_text.append(text)
            # print(" ".join(ocr_text))
            # exit()
            writer.writerow(
                [int(os.path.basename(subfolder)), " ".join(ocr_text)])


if __name__ == "__main__":
    main()
