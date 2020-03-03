from os import walk, path

from matplotlib.pyplot import imread
from cv2 import resize
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import pandas as pd
import numpy as np
import warnings
#warnings.filterwarnings("error")

from face_detector.data_processing.labels import get_face_center_coordinates


class DataGenerator(tf.keras.utils.Sequence):
    def __init__(
        self,
        directory,
        batch_size=32,
        target_size=(480, 640),
        scale_size=1,
        shuffle=True,
        rotation_range=180,
        zoom_range=[0.7, 1.5],
        horizontal_flip=True,
        vertical_flip=True,
        fill_mode="nearest",
    ):

        self.scale_size = scale_size
        self.target_size = target_size
        self.batch_size = batch_size
        self.directory = directory

        self.img_paths = []
        self.img_paths_wo_ext = []
        self.target = []
        self.generator = ImageDataGenerator(
            rotation_range=rotation_range,
            zoom_range=zoom_range,
            horizontal_flip=horizontal_flip,
            vertical_flip=vertical_flip,
            fill_mode=fill_mode,
        )

        for root, dirs, files in walk(directory):
            for file in files:
                if file.lower().endswith(".jpg") or file.lower().endswith(".png"):
                    self.img_paths.append(path.join(root, file))
                    self.img_paths_wo_ext.append(
                        path.splitext(path.join(root, file))[0]
                    )

                elif file.lower().endswith(".txt"):

                    y = get_face_center_coordinates(root, "", file)

                    self.target.append(y)

        self.targets = pd.DataFrame(self.target, columns=["x", "y"])
        self.targets = self.targets.set_index(pd.Index(self.img_paths_wo_ext))

        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        return int(np.floor(len(self.img_paths) / self.batch_size))

    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size : (index + 1) * self.batch_size]

        list_paths = [self.img_paths[k] for k in indexes]
        list_paths_wo_ext = [self.img_paths_wo_ext[k] for k in indexes]
        X, y = self.__data_generation(list_paths, list_paths_wo_ext)

        return X, y

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.img_paths))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_paths, list_paths_wo_ext):
        width, height = self.target_size
        scaled_width, scaled_height = (
            int(width * self.scale_size),
            int(height * self.scale_size),
        )

        X = np.empty(
            (self.batch_size, scaled_width, scaled_height, 3), dtype=np.float32
        )
        y = [
            [int(round(coordinate)) for coordinate in coordinates]
            for coordinates in self.targets.loc[list_paths_wo_ext].values
        ]
        for i, ID in enumerate(list_paths):

            image = resize(imread(ID), (height, width))

            empty_image_with_label = np.empty((width, height, 3), dtype=np.float32)
            random_non_zero_point = [255, 36, 0]
            empty_image_with_label[y[i][1]][y[i][0]] = np.array(random_non_zero_point)

            while True:
                transform_parameters = self.generator.get_random_transform(
                    image, seed=None
                )
                empty_image_with_label = self.generator.apply_transform(
                    empty_image_with_label, transform_parameters
                )
                transformed_label = np.nonzero(empty_image_with_label)
                try:
                    if len(transformed_label[0]) != 0 and len(transformed_label[1]) != 0:
                        y[i][1] = transformed_label[0].mean() * self.scale_size
                        y[i][0] = transformed_label[1].mean() * self.scale_size
                        if isinstance(y[i][0], (int, float)) and isinstance(y[i][1], (int, float)) and y[i][0]!=float('nan') and y[i][1]!=float('nan'):
                            if not isinstance(y[i][0], bool) and not isinstance(y[i][1], bool) and y[i][0]*0 == 0 and y[i][1]*0 == 0:
                                break
                except ValueError:
                    pass

            X[i,] = self.generator.apply_transform(
                resize(image, (scaled_height, scaled_width)), transform_parameters
            )
        return X, np.asarray(y)
