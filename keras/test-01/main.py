#!/usr/bin/env python3
# coding=utf-8
"""A very simple Keras-based NN, for sanity checking.

Depends on the following pure-Python packages:

*   keras
*   tensorflow
"""
import numpy as np
from keras import activations, layers, losses, models, optimizers, utils


def main():
    """Execute business logic."""
    # Create model.
    model = models.Sequential((
        layers.Dense(32, input_shape=(128,), activation=activations.relu),
        layers.Dense(10, activation=activations.softmax),
    ))
    model.compile(
        optimizer=optimizers.SGD(),
        loss=losses.mean_squared_error,
        metrics=['accuracy'],
    )

    # Generate bogus data.
    data = np.random.random((1024, 128))
    labels = np.random.randint(10, size=(1024, 1))

    # Convert labels to categorical one-hot encoding.
    one_hot_labels = utils.to_categorical(labels, num_classes=10)

    # Train the model, iterating on the data in batches of 32 samples.
    model.fit(data, one_hot_labels, epochs=100, batch_size=32)


if __name__ == '__main__':
    main()
