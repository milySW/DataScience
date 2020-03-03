import os
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
from random import sample
from face_detector.data_processing.labels import get_face_center_coordinates


def plot_examples(root_dir, root_listdir, height=4, width=5):
    """
    Function plotting sample from dataset.

    :param str root_dir - images main directory name.
    :param str root_listdir - list of subfolders with images.
    :param int height - number of rows with plots.
    :param int  width - number of columns with plots.
    """
    fig, ax = plt.subplots(height, width, frameon=False, figsize=(20, 20))

    for row_index in range(height):
        for column_index in range(width):
            random_images_dir = np.random.choice(root_listdir)
            random_images_dir_list = os.listdir(root_dir + "/" + random_images_dir)
            var = np.random.randint(3, len(random_images_dir_list) - 2)
            random_image_index = var + var % 2
            img = Image.open(
                root_dir
                + "/"
                + random_images_dir
                + "/"
                + random_images_dir_list[random_image_index]
            )

            random_coordinates_file_index = random_images_dir_list[
                random_image_index
            ].replace("_rgb.jpg", "_pose.txt")
            x_result, y_result = get_face_center_coordinates(
                root_dir, random_images_dir, random_coordinates_file_index
            )

            ax[row_index][column_index].scatter(x_result, y_result, c="red")

            ax[row_index][column_index].imshow(img)
            ax[row_index][column_index].set_xticks([])
            ax[row_index][column_index].set_yticks([])

            plt.tight_layout(pad=0.2, w_pad=0.3, h_pad=0.3)


def random_images(root_dir, number_of_dirs=1, number_of_images=1):
    """
    Function that returns sample of random paths to images.

    :param str root_dir - images main directory name.
    :param int number_of_dirs - the number of dirs from where images will be given
    :param int number_of_images- the number of photos that will be selected from each folder.
    :return list with randomly selected paths to images.
    """
    root_listdir = [
        images_dir
        for images_dir in os.listdir(root_dir)
        if not any(
            characters in images_dir for characters in [".", "test", "train", "valid"]
        )
    ]
    list_of_dir_indices = sample(range(1, len(root_listdir)), number_of_dirs)
    images_paths = []
    for dir_index in list_of_dir_indices:
        paths_list = os.listdir(root_dir + "/" + root_listdir[dir_index])
        number_of_images_in_dir = len(paths_list)
        list_of_images_indices = [
            image_index + image_index % 2
            for image_index in np.random.randint(
                3, len(paths_list) - 2, number_of_images
            )
        ]
        images_paths += [
            root_listdir[dir_index] + "/" + paths_list[image_index]
            for image_index in list_of_images_indices
        ]
    return images_paths


def plot_face(root_dir, x_padding=80, y_padding=120):
    """
    Function plotting sample image with zoom on face.
    :param str root_dir - images main directory name.
    """
    path = random_images(root_dir)
    fig, ax = plt.subplots(1)
    img = Image.open(root_dir + "/" + path[0])
    ax.imshow(img)

    sub_path = path[0].split("/")
    random_images_dir, random_coordinates_file_index = (
        sub_path[0],
        sub_path[1].replace("_rgb.jpg", "_pose.txt"),
    )
    x_result, y_result = get_face_center_coordinates(
        root_dir, random_images_dir, random_coordinates_file_index
    )
    ax.scatter(x_result, y_result, c="red")

    plt.xlim(x_result - x_padding, x_result + x_padding)
    plt.ylim(y_result - y_padding, y_result + y_padding)
    plt.gca().invert_yaxis()
    plt.show()


def plot_one_sample(x, y):
    """
    Function plotting one sample from generator.
    :param numpy.ndarray x - image in array type.
    :param list y - list with the coordinates of the center of the face
    """
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.imshow(x.astype("uint8"))
    ax.scatter(*y)


def plot_many_samples(generator, height=4, width=7, model=None):
    """
    Function plotting samples from generator.
    :param generator generator - custom generator.
    """
    fig, ax = plt.subplots(height, width, figsize=(20, 10))

    x, y = next(iter(generator))
    for row_index in range(height):
        for column_index in range(width):
            ax[row_index][column_index].imshow(
                x[row_index * column_index].astype(np.uint8)
            )
            ax[row_index][column_index].set_xticks([])
            ax[row_index][column_index].set_yticks([])
            ax[row_index][column_index].scatter(*y[row_index * column_index])

            if model is not None:
                ax[row_index][column_index].scatter(
                    *model.predict(
                        np.expand_dims(x[row_index * column_index], axis=0)
                    ).ravel(),
                    c="red"
                )
