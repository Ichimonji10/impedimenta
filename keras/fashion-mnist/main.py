#!/usr/bin/env python3
# coding=utf-8
"""A TensorFlow-based NN that classifies the `fashion MNIST`_ dataset.

Depends on the following pure-Python packages:

*   keras
*   matplotlib
*   tensorflow

This code follows a `guide`_.

.. _fashion mnist: https://github.com/zalandoresearch/fashion-mnist
.. _guide: https://www.tensorflow.org/tutorials/keras/basic_classification
"""
import sys
from typing import Sequence

from tensorflow import keras, nn
import numpy as np

# pylint:disable=wrong-import-position
import matplotlib
matplotlib.use('svg')
from matplotlib import pyplot
# pylint:enable=wrong-import-position

LABEL_NAMES = (
    'T-shirt/top',
    'Trouser',
    'Pullover',
    'Dress',
    'Coat',
    'Sandal',
    'Shirt',
    'Sneaker',
    'Bag',
    'Ankle boot',
)
"""Labels are integers from 0–9, and these are the corresponding names."""


def main() -> None:
    """Execute business logic."""
    (train_images, train_labels), (test_images, test_labels) = (
        keras.datasets.fashion_mnist.load_data()
    )

    # Scale image pixel values from 0–255 to 0–1.
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    # Create and train a model, and use it to generate predictions.
    model = keras.Sequential((
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation=nn.relu),
        keras.layers.Dense(10, activation=nn.softmax),
    ))
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
    )
    model.fit(train_images, train_labels, epochs=5)
    predicted_labels = model.predict(test_images)

    # For the first N test images, plot the image, its predicted label, and the
    # true labe.. Color correct predictions in blue and incorrect predictions
    # in red.
    num_cols = 3
    num_rows = 5
    num_images = num_cols * num_rows
    pyplot.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
    for i in range(num_images):
        pyplot.subplot(num_rows, 2 * num_cols, 2 * i + 1)
        plot_image(predicted_labels[i], test_labels[i], test_images[i])
        pyplot.subplot(num_rows, 2 * num_cols, 2 * i + 2)
        plot_value_array(predicted_labels[i], test_labels[i])
    pyplot.savefig(sys.stdout)


def plot_image(predicted_labels: Sequence[int], label: int, image) -> None:
    """Graph an image, with a label below it."""
    pyplot.grid(False)
    pyplot.xticks(())
    pyplot.yticks(())
    pyplot.imshow(image, cmap=pyplot.cm.binary)
    predicted_label = np.argmax(predicted_labels)
    if predicted_label == label:
        color = 'blue'
    else:
        color = 'red'
    pyplot.xlabel(
        f'{LABEL_NAMES[predicted_label]} '
        f'{100 * np.max(predicted_labels):2.0f}% '
        f'({LABEL_NAMES[label]})',
        color=color
    )


def plot_value_array(predicted_labels: Sequence[int], label: int) -> None:
    """Paint a bar graph showing confidence in each predicted label."""
    pyplot.grid(False)
    pyplot.xticks(())
    pyplot.yticks(())
    this_plot = pyplot.bar(range(10), predicted_labels, color='#777777')
    pyplot.ylim((0, 1))
    predicted_label = np.argmax(predicted_labels)
    this_plot[predicted_label].set_color('red')
    this_plot[label].set_color('blue')


if __name__ == '__main__':
    main()
