
from sklearn.model_selection import StratifiedShuffleSplit

def split_dataset(data, test_size=0.2, class_name='Class'):
    split = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=42)
    for train_index, test_index in split.split(data, data[class_name]):
        strat_train_set = data.loc[train_index]
        strat_test_set = data.loc[test_index]

    X_train = strat_train_set.drop(class_name, axis=1, inplace = False)
    y_train  = strat_train_set[[class_name]]

    X_test = strat_test_set.drop(class_name, axis=1, inplace = False)
    y_test  = strat_test_set[[class_name]]
    
    return X_train, y_train, X_test, y_test
