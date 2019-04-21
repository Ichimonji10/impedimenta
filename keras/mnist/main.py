#!/usr/bin/env python3
# coding=utf-8
"""A NN that classifies the `MNIST database`_ of handwritten digits.

Depends on the following pure-Python packages:

*   keras
*   matplotlib
*   tensorflow

.. _mnist database: https://en.wikipedia.org/wiki/MNIST_database
"""
import argparse
from typing import Sequence

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
        '--nn-type',
        help="""
        The type of neural network to generate. "nn" for a densely-connected
        network of nodes. "cnn" to add convolution.
        """,
        choices=FUNCS.keys(),
        default='nn',
    )
    add_train_flags(parser)
    parser.add_argument(
        '--evaluate',
        help="""
        Print a summary of how well the neural network does on training and
        testing data.
        """,
        action='store_true',
    )
    parser.add_argument(
        '--chart',
        help="""
        Create an SVG chart illustrating some of the training data, and how the
        neural network categorizes it.
        """,
        type=argparse.FileType('w'),
    )
    args = parser.parse_args()

    manager = Manager(args.nn_type)
    if args.train:
        manager.train()
    if args.evaluate:
        print('Performance on test data:')
        for key, val in manager.evaluate().items():
            print(f'{key}: {val}')
    if args.chart:
        manager.chart(args.chart)
        args.chart.close()


def add_train_flags(parser: argparse.ArgumentParser) -> None:
    """Add the ``--{no-,}train`` flags to a parser."""
    # See: https://stackoverflow.com/a/15008806
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--train',
        action='store_true',
        dest='train',
        help="""
        Whether to train the neural network. Should be true in most cases.
        Setting to false can give a baseline sense of what an untrained neural
        network can do.
        """,
    )
    group.add_argument(
        '--no-train',
        action='store_false',
        dest='train',
        help='Inverse of --train',
    )
    group.set_defaults(train=True)


class Manager:
    """A manager that coordinates a nural net and related data.

    :param nn_type: Which type of model to create. If ``nn``, an acyclic neural
        net consisting of `dense`_ layers; if ``cnn``, a convolutional neural
        net; otherwise, raise an exception.
    :raise: ``ValueError`` if ``nn_type`` is not one of the values listed
        above.
    """

    def __init__(self, nn_type: str = 'nn'):
        """Load data and create an untrained neural network."""
        dataset = datasets.mnist.load_data()
        self.train_images = dataset[0][0]
        self.train_labels = dataset[0][1]
        self.test_images = dataset[1][0]
        self.test_labels = dataset[1][1]

        # Images consist of uint8 pixels. Scale values from 0–255 to 0–1.
        self.train_images = self.train_images / 255.0
        self.test_images = self.test_images / 255.0

        # An initially-untrained neural network.
        try:
            func = FUNCS[nn_type]
        except KeyError as err:
            raise ValueError(
                'nn_type must be one of '
                f'{", ".join(str(k) for k in models.keys())}, but is {nn_type}'
            ) from err
        self.nn = func()  # pylint:disable=invalid-name

    def train(self):
        """Train the neural network."""
        self.nn.fit(self.train_images, self.train_labels, epochs=5)

    def evaluate(self):
        """Evaluate the neural network.

        Make sure to train first, or else the neural network will perform
        horribly.

        :return: A dict in the form ``{metric_name: metric}``.
        """
        # One *MUST* call nn.evaluate() before accessing nn.metrics_names.
        metrics = self.nn.evaluate(self.test_images, self.test_labels)
        metrics_names = self.nn.metrics_names
        return dict(zip(metrics_names, metrics))

    def chart(self, handle):
        """Categorize testing data, and chart several of the categorizations.

        Write the chart to the file handle ``handle``.
        """
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
            self._plot_labels(i)
        pyplot.savefig(handle)

    def _plot_image(self, i: int) -> None:
        """Graph an image, with the true label below it."""
        test_image = self.test_images[i]
        test_label: int = self.test_labels[i]

        pyplot.grid(False)
        pyplot.xticks(())
        pyplot.yticks(())
        pyplot.imshow(test_image, cmap=pyplot.cm.binary)
        pyplot.xlabel(f'{test_label}')

    def _plot_labels(self, i: int) -> None:
        """Paint a bar graph showing confidence in each label.

        Below the bar graph, add the name of the label that the NN has the most
        confidence in.
        """
        # An image may have one of ten labels associated with it, where those
        # labels are the ingegers 0–9. When a NN classifies an image, it will
        # output ten integers, each ranging from 0–1, and which add up to 1.
        # predictions_iter is a sequence in the following form:
        #
        # [
        #     [0.1, 0.05, 0.7, 0.01, 0.00, …],  # predict "2"
        #     [0.6, 0.05, 0.1, 0.00, 0.00, …],  # predict "0"
        #     …
        # ]
        predictions_iter: Sequence[Sequence[int]] = (
            self.nn.predict(self.test_images)
        )
        predictions: Sequence[int] = predictions_iter[i]
        prediction_idx = numpy.argmax(predictions)
        prediction = predictions[prediction_idx]
        test_label: int = self.test_labels[i]

        pyplot.grid(False)
        pyplot.xticks(())
        pyplot.yticks(())
        pyplot.xlabel(f'{prediction_idx}, {prediction * 100:2.0f}%')
        pyplot.ylim((0, 1))

        # If set_color() is called on a single bar multiple times, the last
        # call will win.
        this_plot = pyplot.bar(
            range(len(predictions)),
            predictions,
            color='#777777',
        )
        this_plot[prediction_idx].set_color('red')
        this_plot[test_label].set_color('blue')


def _make_nn():
    model = models.Sequential()
    model.add(layers.Flatten())
    model.add(layers.Dense(activation=activations.relu, units=196))  # 28^2 / 4
    model.add(layers.Dense(activation=activations.relu, units=49))  # … / 4
    model.add(layers.Dense(activation=activations.softmax, units=10))
    model.compile(
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
        optimizer='adam',
    )
    return model


def _make_cnn():
    model = models.Sequential()
    model.add(layers.Reshape(
        input_shape=(28, 28),
        target_shape=(28, 28, 1),
    ))
    model.add(layers.Conv2D(
        activation=activations.relu,
        data_format='channels_last',
        filters=32,
        kernel_size=3,
    ))
    model.add(layers.MaxPooling2D())
    model.add(layers.Flatten())
    model.add(layers.Dense(activation=activations.relu, units=128))
    model.add(layers.Dense(activation=activations.softmax, units=10))
    model.compile(
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
        optimizer='adam',
    )
    return model


FUNCS = {'cnn': _make_cnn, 'nn': _make_nn}
"""Functions for generating neural networks."""


if __name__ == '__main__':
    main()
