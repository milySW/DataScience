from itertools import permutations
import shutil
import numpy as np
import os


def find_closest_sum(numbers, target, n):
    """
    Function finding best combination of n dirs to cover given target.

    :param int numbers - list with numbers
    :param int target - number to estimate with elements of given list
    :param int n - number of elements used in task
    :return tuple with best combination
    """
    permutations_list = list(permutations(numbers, n))
    sumlist = [np.sum(permutation) for permutation in permutations_list]
    max_position = 0
    for index in range(1, len(sumlist)):
        if abs(sumlist[index] - target) < abs(sumlist[max_position] - target):
            max_position = index

    return permutations_list[max_position]


def best_sum(numbers, target):
    """
    Function finding best combination of dirs to cover given target.

    :param int numbers - list with numbers
    :param int target - number to estimate with elements of given list
    :return list of best combination
    """
    result = 0
    for number_of_dirs_in_combination in range(1, len(numbers) + 1):
        previous = result
        result = find_closest_sum(numbers, target, number_of_dirs_in_combination)
        if number_of_dirs_in_combination > 1 and np.sum(result) > target:
            return list(previous)
        elif number_of_dirs_in_combination == 1 and np.sum(result) > target:
            return list(result)
    return list(numbers)


def find_and_remove(available_number_of_images_in_dir_list, target, name):
    """
    Function finding best combination of dirs to cover given target and removing combination elements from given list.

    :param int available_number_of_images_in_dir_list - list with numbers of images in dirs
    :param int target - number to estimate with elements of given list
    :param str name - name of set, used in print
    :return
        best - best combination of dirs to cover given images number
        available_number_of_images_in_dir_list - list given in argument without numbers of images selected into best
    """
    best = best_sum(available_number_of_images_in_dir_list, target)
    print(name, " set size: ", np.sum(best))
    for list_element in best:
        available_number_of_images_in_dir_list.remove(list_element)
    return best, available_number_of_images_in_dir_list


def my_make_dir(directory):
    """
    Function create directory if not exist.

    :param str directory - name of directory to create
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def images_train_test_split(root_dir, test_ratio, valid_ratio, mode=1):
    """
    Function finding best combination of dirs to cover given images ratio.

    :param str root_dir - images main directory name.
    :param float test_ratio - ratio of dirs/images in test set
    :param float valid_ratio - ratio of dirs/images in valid set
    :param int mode - 1 is for learning by dirs number ratio,
    2 is fore learning by images number ratio
    :return
        test_size - number of images in test_set
        valid_size - number of images in valid_set
        train_size - number of images in train_set
    """
    number_of_images_in_dir_list = []
    root_listdir = [
        dir_name
        for dir_name in os.listdir(root_dir)
        if not any(
            characters in dir_name for characters in [".", "test", "train", "valid"]
        )
    ]

    for dir_name in root_listdir:
        number_of_images_in_dir_list.append(
            len(os.listdir(root_dir + "/" + dir_name)) / 2 - 2
        )

    if mode == 1:
        root_listdir_length = len(root_listdir)

        best_test = number_of_images_in_dir_list[
            : int(root_listdir_length * test_ratio)
        ]
        test_size = np.sum(best_test)
        print("Test set size: ", test_size)

        best_valid = number_of_images_in_dir_list[
            int(root_listdir_length * test_ratio) : int(
                root_listdir_length * test_ratio
            )
            + int(root_listdir_length * test_ratio)
        ]
        valid_size = np.sum(best_valid)
        print("Valid set size: ", valid_size)

        best_train = number_of_images_in_dir_list[
            int(root_listdir_length * test_ratio)
            + int(root_listdir_length * test_ratio) :
        ]
        train_size = np.sum(best_train)
        print("Train set size: ", train_size)

    elif mode == 2:
        summ = np.sum(list(number_of_images_in_dir_list))

        available_number_of_images_in_dir_list = number_of_images_in_dir_list.copy()

        test_size = round(summ * test_ratio)
        valid_size = round(summ * valid_ratio)
        train_size = summ - test_size - valid_size

        best_test, available_number_of_images_in_dir_list = find_and_remove(
            available_number_of_images_in_dir_list, test_size, "Test"
        )
        best_valid, available_number_of_images_in_dir_list = find_and_remove(
            available_number_of_images_in_dir_list, valid_size, "Validation"
        )
        best_train = available_number_of_images_in_dir_list

        test_size = np.sum(best_test)
        valid_size = np.sum(best_valid)
        train_size = np.sum(best_train)

        print("Train set size: ", test_size)

    train_folder = root_dir + "/train"
    test_folder = root_dir + "/test"
    valid_folder = root_dir + "/valid"

    my_make_dir(train_folder)
    my_make_dir(test_folder)
    my_make_dir(valid_folder)

    for index, number_of_images_in_dir in enumerate(number_of_images_in_dir_list):
        if number_of_images_in_dir in best_test:
            shutil.move(root_dir + "/" + root_listdir[index], test_folder)
            best_test.remove(number_of_images_in_dir)
        elif number_of_images_in_dir in best_valid:
            shutil.move(root_dir + "/" + root_listdir[index], valid_folder)
            best_valid.remove(number_of_images_in_dir)
        elif number_of_images_in_dir in best_train:
            shutil.move(root_dir + "/" + root_listdir[index], train_folder)
            best_train.remove(number_of_images_in_dir)

    return test_size, valid_size, train_size
