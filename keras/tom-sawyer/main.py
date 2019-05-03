import io
import sys
import random

import numpy as np
from keras.models import Sequential
from keras.utils.data_utils import get_file


def main():
    path = get_file(
        '74-0.txt',
        origin='https://www.gutenberg.org/files/74/74-0.txt')
    with io.open(path, encoding='utf-8') as f:
        raw_text = f.read()
    text = raw_text[raw_text.index('CHAPTER I\n\n'):raw_text.index('End of the Project Gutenberg Ebook')]
    And to prepare the text for training, use
    chars = sorted(list(set(text)))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))
    maxlen = 40
    step = 2
    sentences = []
    next_chars = []
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])
    x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1


if __name__ == '__main__':
    main()
