import numpy as np
import pandas as pd

def n_data_splits(data_train, columns, n):
    data_train_1 = data_train[data_train['Class'] == -1]
    data_train_0 = data_train[data_train['Class'] == 1]

    border = int(len(data_train_0)/n)
    indices = [i*border for i in range(n)]
    indices = indices + [len(data_train_0) - 1]

    data_train_0_chunks = [data_train_0.iloc[indices[n]:indices[n+1]] for n in range(len(indices)-1)]

    list_of_training_sets = []
    col_names = list(columns)
    col_names.pop()

    for i in data_train_0_chunks:
        var = pd.concat([i, data_train_1])
        var_y = var['Class']
        var_X = var[col_names]
        list_of_training_sets.append([var_X, var_y])
    
    return list_of_training_sets
