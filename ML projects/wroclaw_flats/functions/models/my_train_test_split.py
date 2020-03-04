from sklearn.model_selection import StratifiedShuffleSplit


def my_train_test_split(data, target_name, groupby, names_to_drop, dropgroupby=False):
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    data = data.drop(names_to_drop, axis=1)
    data = data.dropna()
    for train_index, test_index in split.split(data, data[groupby]):
        strat_train_set = data.reindex(train_index).dropna()
        strat_test_set = data.reindex(test_index).dropna()

    y_train = strat_train_set[[target_name]]
    X_train = strat_train_set.drop(target_name, axis=1, inplace=False)

    y_test = strat_test_set[[target_name]]
    X_test = strat_test_set.drop(target_name, axis=1, inplace=False)

    if dropgroupby:
        X_train = X_train.drop(groupby, axis=1)
        X_test = X_test.drop(groupby, axis=1)
    return X_train, X_test, y_train, y_test
