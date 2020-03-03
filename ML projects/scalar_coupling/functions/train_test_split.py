import os
import numpy as np
import pandas as pd


def train_test_split(data, groupby):
    data_list = os.listdir(os.getcwd() + "/data")
    if "train_set.csv" in data_list and "test_set.csv" in data_list:
        train = pd.read_csv("data/train_set.csv")
        test = pd.read_csv("data/test_set.csv")
    else:
        unique_molecules = data[groupby].unique()
        train_molecules, test_molecules = np.split(
            np.random.permutation(unique_molecules), [int(0.8 * len(unique_molecules))]
        )

        test = data[data[groupby].isin(test_molecules)]
        train = data[data[groupby].isin(train_molecules)]
        train.to_csv(r"data/train_set.csv", encoding="utf-8", index=False)
        test.to_csv(r"data/test_set.csv", encoding="utf-8", index=False)
    return train, test
