# imports
import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import lightgbm as lgb

from sklearn import metrics
from sklearn.model_selection import KFold


def group_mean_log_mae(y_true, y_pred, types, floor=1e-9):
    """
    Fast metric computation for this competition: https://www.kaggle.com/c/champs-scalar-coupling
    Code is from this kernel: https://www.kaggle.com/uberkinder/efficient-metric
    """
    maes = (y_true - y_pred).abs().groupby(types).mean()
    return np.log(maes.map(lambda x: max(x, floor))).mean()

def save_obj(obj, name):
    with open("obj/" + name + ".pkl", "wb") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open("obj/" + name + ".pkl", "rb") as f:
        return pickle.load(f)


def train_model_regression(
    X,
    X_test,
    y,
    params,
    model_name,
    models_dir,
    folds=KFold(n_splits=5, shuffle=True, random_state=11),
    model_type="lgb",
    eval_metric="mae",
    columns=None,
    plot_feature_importance=False,
    model=None,
    verbose=10000,
    early_stopping_rounds=200,
    n_estimators=50000,
    n=5,
):
    """
    A function to train a variety of regression models.
    Returns dictionary with oof predictions, test predictions, scores and, if necessary, feature importances.
    
    :params: X - training data, can be pd.DataFrame or np.ndarray (after normalizing)
    :params: X_test - test data, can be pd.DataFrame or np.ndarray (after normalizing)
    :params: y - target
    :params: folds - folds to split data
    :params: model_type - type of model to use
    :params: eval_metric - metric to use
    :params: columns - columns to use. If None - use all columns
    :params: plot_feature_importance - whether to plot feature importance of LGB
    :params: model - sklearn model, works only for "sklearn" model type
    :params: model_name - name of file where model will be saved
    :params: models_dir - path to models directory
    :params: n - number of folds
    """
    columns = X.columns if columns is None else columns
    X_test = X_test[columns]

    if model_name + ".sav" in os.listdir(models_dir):
        regressor = pickle.load(open(models_dir + "/" + model_name + ".sav", "rb"))
        result_dict = load_obj("result_dict_" + model_name)
        return regressor, result_dict

    # to set up scoring parameters
    metrics_dict = {
        "mae": {
            "lgb_metric_name": "mae",
            "sklearn_scoring_function": metrics.mean_absolute_error,
        },
        "group_mae": {
            "lgb_metric_name": "mae",
            "scoring_function": group_mean_log_mae,
        },
        "mse": {
            "lgb_metric_name": "mse",
            "sklearn_scoring_function": metrics.mean_squared_error,
        },
    }

    result_dict = {}

    # out-of-fold predictions on train data
    oof = np.zeros(len(X))

    # averaged predictions on train data
    prediction = np.zeros(len(X_test))

    # list of scores on folds
    scores = []
    feature_importance = pd.DataFrame()

    # split and train on folds
    for fold_n, (train_index, valid_index) in enumerate(folds.split(X)):
        print(f"Fold {fold_n + 1} started at {time.ctime()}")
        if type(X) == np.ndarray:
            X_train, X_valid = X[columns][train_index], X[columns][valid_index]
            y_train, y_valid = y[train_index], y[valid_index]
        else:
            X_train, X_valid = (
                X[columns].iloc[train_index],
                X[columns].iloc[valid_index],
            )
            y_train, y_valid = y.iloc[train_index], y.iloc[valid_index]

        if model_type == "lgb":
            model = lgb.LGBMRegressor(**params, n_estimators=n_estimators, n_jobs=-1)
            model.fit(
                X_train,
                y_train,
                eval_set=[(X_train, y_train), (X_valid, y_valid)],
                eval_metric=metrics_dict[eval_metric]["lgb_metric_name"],
                verbose=verbose,
                early_stopping_rounds=early_stopping_rounds,
            )

            y_pred_valid = model.predict(X_valid)
            y_pred = model.predict(X_test, num_iteration=model.best_iteration_)

        if model_type == "sklearn":
            model = model
            model.fit(X_train, y_train)

            y_pred_valid = model.predict(X_valid).reshape(-1,)
            score = metrics_dict[eval_metric]["sklearn_scoring_function"](
                y_valid, y_pred_valid
            )
            print(f"Fold {fold_n}. {eval_metric}: {score:.4f}.")
            print("")

            y_pred = model.predict(X_test).reshape(-1,)


        oof[valid_index] = y_pred_valid.reshape(-1,)
        if eval_metric != "group_mae":
            scores.append(
                metrics_dict[eval_metric]["sklearn_scoring_function"](
                    y_valid, y_pred_valid
                )
            )
        else:
            scores.append(
                metrics_dict[eval_metric]["scoring_function"](
                    y_valid, y_pred_valid, X_valid["type"]
                )
            )

        prediction += y_pred

        if model_type == "lgb" and plot_feature_importance:
            # feature importance
            fold_importance = pd.DataFrame()
            fold_importance["feature"] = columns
            fold_importance["importance"] = model.feature_importances_
            fold_importance["fold"] = fold_n + 1
            feature_importance = pd.concat(
                [feature_importance, fold_importance], axis=0
            )

    prediction /= folds.n_splits

    print(
        "CV mean score: {0:.4f}, std: {1:.4f}.".format(np.mean(scores), np.std(scores))
    )

    result_dict["oof"] = oof
    result_dict["prediction"] = prediction
    result_dict["scores"] = scores

    if model_type == "lgb":
        if plot_feature_importance:
            feature_importance["importance"] /= folds.n_splits
            cols = (
                feature_importance[["feature", "importance"]]
                .groupby("feature")
                .mean()
                .sort_values(by="importance", ascending=False)[:50]
                .index
            )

            best_features = feature_importance.loc[
                feature_importance.feature.isin(cols)
            ]

            plt.figure(figsize=(16, 12))
            sns.barplot(
                x="importance",
                y="feature",
                data=best_features.sort_values(by="importance", ascending=False),
            )
            plt.title("LGB Features (avg over folds)")

            result_dict["feature_importance"] = feature_importance

    filename = models_dir + "/" + model_name + ".sav"
    pickle.dump(model, open(filename, "wb"))
    save_obj(result_dict, "result_dict_" + model_name)

    return model, result_dict


def scored_df(scores_list):
    folds_n = len(scores_list)
    columns = ["Fold_" + str(i) for i in range(1, folds_n + 1)]
    scores_pd = pd.DataFrame(np.array(scores_list).reshape(1, -1), columns=columns)
    return scores_pd
