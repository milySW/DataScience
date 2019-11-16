import shutil
import numpy as np
import os


def split_images(root_listdir, root_dir, sub_dir_name):
    """
    Function splitting images into train, valid and test sets.
    :param list root_listdir - list of image names
    :param str root_dir - root directory for train, valid and test directories
    :param str sub_dir_name - subdirectory name(works as label)
    :return
        int train_examples - number of images in train set, 
        int valid_examples - number of images in valid set, 
        int test_examples - number of images in test set.
    """
    len_data = len(root_listdir)
    train_set = 0.7
    train_examples = round(len_data * train_set)
    valid_examples = round((len_data - train_examples) * 0.5)
    test_examples = len_data - train_examples - valid_examples

    # randomly choose training and testing cases
    permutation = np.random.permutation(len_data)
    train_set = [root_listdir[i] for i in permutation[:][:train_examples]]
    test_set = [root_listdir[i] for i in permutation[train_examples:-valid_examples]]
    valid_set = [root_listdir[i] for i in permutation[-valid_examples:]]

    train_folder = root_dir + "/train"
    test_folder = root_dir + "/test"
    valid_folder = root_dir + "/valid"

    os.makedirs(train_folder + sub_dir_name)
    os.makedirs(test_folder + sub_dir_name)
    os.makedirs(valid_folder + sub_dir_name)

    for f in train_set:
        shutil.move(root_dir + "/" + f, train_folder + sub_dir_name)
        
    for f in test_set:
        shutil.move(root_dir + "/" + f, test_folder + sub_dir_name)
        
    for f in valid_set:
        shutil.move(root_dir + "/" + f, valid_folder + sub_dir_name)


    return train_examples, valid_examples, test_examples
