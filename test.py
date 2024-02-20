from common import read_file, words
from PIL import Image

if __name__ == '__main__':
    img_path = 'ci_1_9.png'
    img = Image.open(img_path)
    for i, (word, pos) in enumerate(words(read_file(img_path, mode='rb'))):
        print(i, word, pos)
