from keras.preprocessing.image import ImageDataGenerator


def my_image_data_generator(
    folder_name,
    batch_size=32,
    img_height=224,
    img_width=224,
    channels=3,
    shuffle=False,
    class_mode="categorical",
    classes=None,
):
    """
    Function is a shortcut to create images generator.
    
    :param str folder_name - path to the folder with images
    :param int batch_size - number of images in batch
    :param img_height - height of loaded images
    :param img_width - width of loaded images
    :param int channels - number of channels in image
    :param bool shuffle - determine if images are shuffled
    
    :return keras.preprocessing.image.DirectoryIterator my_generator - generator of images in given direcotry.
    """
    my_generator = ImageDataGenerator(
        rescale=1.0 / 255, rotation_range=5, zoom_range=0.2, horizontal_flip=True
    ).flow_from_directory(
        folder_name,
        color_mode="rgb",
        target_size=(img_height, img_width),
        batch_size=batch_size,
        classes=classes,
        class_mode=class_mode,
        shuffle=shuffle,
    )

    return my_generator
