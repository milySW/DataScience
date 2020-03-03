import os
from PIL import Image


def my_root_listdir(root_dir):
    """
    Method counting photos and creatig list of subfolders with images.
    
    :param str root_dir - images main directory name.
    :return list of subfolders with images.
    """
    root_listdir = [
        images_dir
        for images_dir in os.listdir(root_dir)
        if not any(
            characters in images_dir for characters in [".", "test", "train", "valid"]
        )
    ]
    summ = 0
    for images_dir in root_listdir:
        summ += len(os.listdir(root_dir + "/" + images_dir)) / 2 - 2
    print("Sum of images in directories: ", int(summ))
    return root_listdir


def verify_images(root_dir, root_listdir):
    """
    Method opening all images to test their validity.
    
    :param str root_dir - images main directory name.
    :param str root_listdir - list of subfolders with images.
    """
    counter = 0

    for index, image_dir in enumerate(root_listdir):
        images_listdir = os.listdir(root_dir + "/" + image_dir)
        list_of_images_indices = [
            image_index
            for image_index in range(3, len(images_listdir) - 1)
            if image_index % 2 == 0
        ]
        for image_ind in list_of_images_indices:
            filename = root_dir + "/" + image_dir + "/" + images_listdir[image_ind]
            try:
                im = Image.open(filename)
                im.verify()
                im.close()
            except (OSError, ValueError):
                counter += 1

    print("%d files caused error due to OSError and  ValueError." % counter)
