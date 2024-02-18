import ddddocr
from common import read_file

if __name__ == '__main__':
    ocr = ddddocr.DdddOcr()

    png = read_file('./a1.png', mode='rb')

    print(ocr.classification(png))
