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
import argparse
from typing import Optional, Sequence

import numpy
from keras import activations, datasets, layers, models

# pylint:disable=wrong-import-position
import matplotlib
matplotlib.use('svg')
from matplotlib import pyplot
# pylint:enable=wrong-import-position


def main() -> None:
    """Parse CLI arguments and call business logic."""
    parser = argparse.ArgumentParser(
        description='Classify images with a neural network.',
    )
    parser.add_argument(
        '--chart',
        help="""
        Chart a subset of the neural network's predictions at this path.
        """,
        type=argparse.FileType('w'),
    )
    args = parser.parse_args()

    manager = Manager()
    manager.predict()
    if args.chart:
        manager.chart(args.chart)
        args.chart.close()


class Manager:
    """A manager that coordinates a neural neta and related data.

    The suggested usage pattern is to call ``predict()`` to generate
    predictions, then ``chart()`` to visualize them. This class was sloppily
    slapped together to solve data sharing issues.
    """

    def __init__(self):
        """Load data into memory, and munge it."""
        train, test = datasets.fashion_mnist.load_data()
        self.train_images = train[0]
        self.train_labels = train[1]
        self.test_images = test[0]
        self.test_labels = test[1]

        # Scale image pixel values from 0–255 to 0–1.
        self.train_images = self.train_images / 255.0
        self.test_images = self.test_images / 255.0

        # Labels are integers from 0–9, and these are the corresponding names.
        self.label_names = (
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

        # A prediction is an integer from 0–1, denoting the NN's confidence
        # that an image is associated with a label. A sequence of predictions
        # should add up to one.
        #
        # There is a sequence of predictions for each test image.
        self.predictions_iter: Optional[Sequence[Sequence[int]]] = None

    def predict(self):
        """Create and train a model, and use it to generate predictions.

        Throw away the model, and save the predictions.
        """
        model = models.Sequential((
            layers.Flatten(input_shape=(28, 28)),
            layers.Dense(128, activation=activations.relu),
            layers.Dense(10, activation=activations.softmax),
        ))
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'],
        )
        model.fit(self.train_images, self.train_labels, epochs=5)
        self.predictions_iter = model.predict(self.test_images)

    def chart(self, handle):
        """Chart several predictions created by this neural net.

        Write the chart to the file handle ``handle``. If no predictions have
        been created with ``predict()``, create some.
        """
        if self.predictions_iter is None:
            self.predict()

        # For the first several test images, plot the image, its predicted
        # label, and the true label. Color correct predictions in blue and
        # incorrect predictions in red.
        num_cols = 3
        num_rows = 5
        num_images = num_cols * num_rows
        pyplot.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
        for i in range(num_images):
            pyplot.subplot(num_rows, 2 * num_cols, 2 * i + 1)
            self._plot_image(i)
            pyplot.subplot(num_rows, 2 * num_cols, 2 * i + 2)
            self._plot_value_array(i)
        pyplot.savefig(handle)

    def _plot_image(self, i: int) -> None:
        """Graph an image, with a label below it."""
        predictions = self.predictions_iter[i]
        test_label = self.test_labels[i]
        test_image = self.test_images[i]

        pyplot.grid(False)
        pyplot.xticks(())
        pyplot.yticks(())
        pyplot.imshow(test_image, cmap=pyplot.cm.binary)
        prediction = numpy.argmax(predictions)
        if prediction == test_label:
            color = 'blue'
        else:
            color = 'red'
        pyplot.xlabel(
            f'{self.label_names[prediction]} '
            f'{100 * numpy.max(predictions):2.0f}% '
            f'({self.label_names[test_label]})',
            color=color
        )


    def _plot_value_array(self, i: int) -> None:
        """Paint a bar graph showing confidence in each predicted label."""
        predictions = self.predictions_iter[i]
        prediction = numpy.argmax(predictions)
        test_label = self.test_labels[i]

        pyplot.grid(False)
        pyplot.xticks(())
        pyplot.yticks(())
        this_plot = pyplot.bar(
            range(len(predictions)),
            predictions,
            color='#777777',
        )
        pyplot.ylim((0, 1))

        # If the NN's predicted label and the true label are for the same bar,
        # then the second set_color() call with win.
        this_plot[prediction].set_color('red')
        this_plot[test_label].set_color('blue')


if __name__ == '__main__':
    main()
