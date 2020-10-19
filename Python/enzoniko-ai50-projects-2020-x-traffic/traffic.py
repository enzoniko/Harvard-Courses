import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    # Empty images and labels list
    images, labels = list(), list()

    # Walk trough the data_dir directory
    for root, subdirectories, files in os.walk(data_dir):

        # For each subdirectory
        # sorted(subdirectories, key = lambda category: int(category))
        for subdirectory in subdirectories:

            # For each image in the subdirectory
            # Use os.path.join for platform-independence 
            for image in os.listdir(os.path.join(root, subdirectory)):
                # Use imread() cv2 function to read the image (it returns a numpy.ndarray)
                # Use cv2.resize to make all images (that were read) the same size
                # Read the image as a numpy multidimensional array and resize it accordingly
                image = cv2.resize(cv2.imread(os.path.join(root, subdirectory, image), 1), (IMG_WIDTH, IMG_HEIGHT))

                # Append the resized image to the images list
                images.append(image)
            
                # Append the subdirectory name as an integer to the labels list
                labels.append(int(subdirectory))

    # Return the images and the labels
    return images, labels

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    # Create a convolutional neural network
    model = tf.keras.models.Sequential([

        # Convolutional layer. Learn 32 filters using a 3x3 kernel  
        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Max-pooling layer, using 3x3 pool size
        tf.keras.layers.MaxPooling2D(pool_size=(3, 3)),

        # Add a hidden layer with dropout
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="sigmoid"),
        tf.keras.layers.Dropout(0.2),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add output layer with NUM_CATEGORIES outputs
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="sigmoid")

    ])

    # Train neural network
    model.compile(
        optimizer="nadam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    # Return the model
    return model


if __name__ == "__main__":
    main()
