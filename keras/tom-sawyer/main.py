#!/usr/bin/env python3
# coding=utf-8
"""Train a neural net on Tom Sawyer, and use it to generate prose.

Beware that this code is inefficient, and was written by someone who has a poor
understanding of neural nets.
"""
import random
from typing import Iterator, List, Mapping, Optional, Sequence

import numpy as np
from keras import activations, callbacks, layers, models, optimizers, utils


def main() -> None:
    """Coordinate business logic."""
    text = get_text()
    max_sentence_len = 40
    manager = Manager(text, max_sentence_len)
    callback = callbacks.LambdaCallback(
        on_epoch_end=on_epoch_end_func(manager)
    )
    manager.train(epochs=10, callbacks_=[callback])


class Manager:
    """A manager that coordinates a neural net and related data."""

    def __init__(self, text: str, max_sentence_len: int) -> None:
        """Set instance variables."""
        self.text: str = text
        self.max_sentence_len: int = max_sentence_len

        # Collect all unique characters that appear in the text.
        self.chars: List[str] = list(set(text))
        self.chars.sort()
        self.char_indices: Mapping[str, int] = {
            char: i for i, char in enumerate(self.chars)
        }

        # Create an untrained neural net.
        self.nn = self._make_nn()  # pylint:disable=invalid-name

    def _make_nn(self):
        # Compile a neural net. Batches from the input matrix are fed into the
        # neural net, where each batch is created by slicing on the X axis.
        # Therefore, the X axis doesn't need to be listed as part of the
        # input_shape.
        input_shape = (self.max_sentence_len, len(self.chars))

        # Using an LSTM seems like a reasonable choice given:
        # http://karpathy.github.io/2015/05/21/rnn-effectiveness/
        model = models.Sequential((
            layers.LSTM(128, input_shape=input_shape),
            layers.Dense(len(self.chars), activation=activations.softmax),
        ))
        model.compile(
            loss='categorical_crossentropy',
            metrics=['accuracy'],
            optimizer=optimizers.RMSprop(lr=0.01),
        )
        return model

    def train(
            self,
            epochs: int = 1,
            callbacks_: Optional[Sequence[callbacks.Callback]] = None) -> None:
        """Train the neural net.

        :param epochs: The number of epochs of training to perform. Training
            has a start-up cost, so performing several epochs of training
            back-to-back is more efficient.
        :param callbacks_: A sequence of callbacks pass to `fit`_. See
            `callbacks`_.

        .. _callbacks: https://keras.io/callbacks/
        .. _fit: https://keras.io/models/sequential/#fit
        """
        # Build "sentences", and track the next character for each sentence. For
        # example, one might come up with a sentence of text[0:40] with a next char
        # of text[40].
        sentences = []
        next_chars = []
        step = 2
        for i in range(0, len(self.text) - self.max_sentence_len, step):
            sentences.append(self.text[i: i + self.max_sentence_len])
            next_chars.append(self.text[i + self.max_sentence_len])

        # Inputs is a 3D matrix, where the X coordinate selects a sentence, the Y
        # coordinate selects a character within that sentence, and the Z axis
        # selects that character's ID.
        encoded_sentences = np.zeros(
            (len(sentences), self.max_sentence_len, len(self.chars)),
            dtype=np.bool
        )

        # Outputs is a 2D matrix,  where the X coordinate selects a sentence, and
        # the Y coordinate selects the next character's ID.
        encoded_next_chars = np.zeros(
            (len(sentences), len(self.chars)),
            dtype=np.bool
        )

        # Populate the matrices.
        for sentences_idx, sentence in enumerate(sentences):
            for sentence_idx, char in enumerate(sentence):
                encoded_sentences[
                    sentences_idx,
                    sentence_idx,
                    self.char_indices[char]
                ] = 1
            encoded_next_chars[
                sentences_idx,
                self.char_indices[next_chars[sentences_idx]]
            ] = 1

        # Train the neural net!
        self.nn.fit(
            encoded_sentences,
            encoded_next_chars,
            epochs=epochs,
            callbacks=callbacks_,
        )

    def hallucinate(self, seed: Optional[str] = None) -> Iterator[str]:
        """Given some seed text, generate additional characters.

        The seed could be one of the sentences used for training, but it
        shouldn't be restricted to just them, as the sentences used for
        training could have been generated with a step size greater than 1.

        :param seed: A slice of text used to initialize the neural net. Each
            time the neural net generates a character, the seed's first
            character is dropped, and the new character is appended to the
            seed. (Strings are immutable, and this parameter isn't modified.)
        :return: An iterator that yields the characters generated by the neural
            net. There's no limit to the number of characters that can be
            yielded.
        """
        if seed is None:
            seed = self.get_seed()

        while True:
            # Create a matrix from the seed sentence, where the matrix has the same
            # structure as the input training data.
            encoded_seed = np.zeros(
                (1, self.max_sentence_len, len(self.chars)),
                dtype=np.bool,
            )
            for i, char in enumerate(seed):
                encoded_seed[0, i, self.char_indices[char]] = 1

            # For every character, calculate the likelihood of that character
            # appearing next.
            char_probs = self.nn.predict(encoded_seed)[0]

            # Pick a character. Tend toward more probable characters, but don't
            # pick *the* most probable character *every* time.
            chosen_char_prob = np.random.choice(char_probs, p=char_probs)
            chosen_char_prob_idx = np.where(char_probs == chosen_char_prob)[0][0]
            chosen_char = self.chars[chosen_char_prob_idx]

            seed = seed[1:] + chosen_char
            yield chosen_char

    def get_seed(self) -> str:
        """Select a random slice from ``self.text``.

        :return: A random slice from ``self.text``, of length
            ``self.max_sentence_len``.
        """
        start_index: int = random.randint(
            0,
            len(self.text) - self.max_sentence_len,
        )
        end_index: int = start_index + self.max_sentence_len
        return self.text[start_index:end_index]


def get_text() -> str:
    """Get the contents of Tom Sawyer."""
    # utils.get_file() caches downloads.
    path = utils.get_file(
        '74-0.txt',
        origin='https://www.gutenberg.org/files/74/74-0.txt',
    )
    with open(path) as handle:
        text: str = handle.read()
    start_index: int = text.index('CHAPTER I\n\n')
    end_index: int = text.index('End of the Project Gutenberg Ebook')
    return text[start_index:end_index]


def on_epoch_end_func(manager):
    """Generate a function to be used with the ``on_epoch_end`` callback.

    See :meth:`Manager.train`.
    """

    def on_epoch_end(epoch: int, _):
        print(f'Epoch {epoch} hallucination:')
        gen = manager.hallucinate()
        for _ in range(512):
            print(next(gen), end='')
        print()

    return on_epoch_end


if __name__ == '__main__':
    main()
