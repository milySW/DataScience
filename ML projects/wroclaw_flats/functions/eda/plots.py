import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import itertools

from yellowbrick.regressor import ResidualsPlot
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, export_graphviz
from IPython.display import SVG
from graphviz import Source
from IPython.display import display
from ipywidgets import interactive


def olx_histograms(data, col_names):
    fig = plt.figure(figsize=(20, 5))
    ax = fig.gca()
    col_names = ["Date", "Time", "Furnished", "Sold_in_30"]

    hist_data = data[col_names].dropna()
    hist_data["Date"] = [i[1] for i in hist_data["Date"].str.split(".")]

    bar_width = 0.8

    for num, col in enumerate(col_names[:-1]):
        base = sorted([i for i in hist_data[col].unique() if type(i) != float])

        if col == "Time":
            base.pop()

        y_pos = np.arange(len(base))
        performance = [list(hist_data[col]).count(i) for i in base]

        group_1 = hist_data[col]
        performance_1 = [list(group_1).count(i) for i in base]

        group_2 = hist_data[col][hist_data["Sold_in_30"] == 1].append(pd.Series(base))
        performance_2 = [list(group_2).count(i) for i in base]

        plt.subplot(1, 3, num + 1)

        plt.bar(
            y_pos, performance_1, color="steelblue", edgecolor="black", width=bar_width
        )
        plt.bar(y_pos, performance_2, color="red", edgecolor="black", width=bar_width)

        plt.title(col)
        plt.xticks(y_pos, base)

    plt.tight_layout(rect=(0, 0, 1.2, 1.2))
    plt.show()


def plot_histograms(data, col_names_to_delete=None):
    fig = plt.figure(figsize=(20, 11))
    ax = fig.gca()
    col_names = list(data.columns.values)
    for i in col_names_to_delete:
        col_names.remove(i)
    hist_data_2 = data[col_names].dropna()

    for num, col in enumerate(col_names):
        plt.subplot(3, 4, num + 1)

        if col in ["Price", "Area"]:
            plt.hist(
                hist_data_2[col],
                bins=12,
                color="steelblue",
                edgecolor="black",
                linewidth=0.5,
                align="mid",
            )
            plt.hist(
                hist_data_2[col][hist_data_2["Sold_in_30"] != 2],
                bins=12,
                color="magenta",
                edgecolor="black",
                linewidth=0.5,
                range=[min(hist_data_2[col]), max(hist_data_2[col])],
                align="mid",
            )
            plt.hist(
                hist_data_2[col][hist_data_2["Sold_in_30"] == 1],
                bins=12,
                color="red",
                edgecolor="black",
                linewidth=0.5,
                range=[min(hist_data_2[col]), max(hist_data_2[col])],
                align="mid",
            )
        else:
            base = sorted([i for i in data[col].unique() if type(i) != float])
            y_pos = np.arange(len(base))

            if col == "Sold_in_30":
                performance = [list(hist_data_2[col]).count(i) for i in base]
                plt.bar(
                    y_pos,
                    performance,
                    align="center",
                    color=("magenta", "red", "steelblue"),
                    edgecolor="black",
                )

            else:
                bar_width = 0.8
                if len(base) <= 2:
                    bar_width = 0.4

                group_1 = hist_data_2[col]
                performance_1 = [list(group_1).count(i) for i in base]

                group_2 = hist_data_2[col][hist_data_2["Sold_in_30"] != 2].append(
                    pd.Series(base)
                )
                performance_2 = [list(group_2).count(i) for i in base]

                group_3 = hist_data_2[col][hist_data_2["Sold_in_30"] == 1].append(
                    pd.Series(base)
                )
                performance_3 = [list(group_3).count(i) for i in base]

                plt.bar(
                    y_pos,
                    performance_1,
                    color="steelblue",
                    edgecolor="black",
                    width=bar_width,
                )
                plt.bar(
                    y_pos,
                    performance_2,
                    color="magenta",
                    edgecolor="black",
                    width=bar_width,
                )
                plt.bar(
                    y_pos,
                    performance_3,
                    color="red",
                    edgecolor="black",
                    width=bar_width,
                )

            plt.xticks(y_pos, base)

            if col in ["Location", "Dealer", "Floor", "Building"]:
                plt.xticks(rotation="vertical")

        # niebieski 2 - oferty, które nie zeszły i młodsze niż 30 dni.
        # czerwony 1 - oferty, które zeszły w czasie poniżej 30 dni.
        # magenta 0 - oferty, które nie zeszły w ciągu 30 dni.
        plt.title(col)

    plt.tight_layout(rect=(0, 0, 1.2, 1.2))
    plt.show()


def plot_heatmap(data, col_names):
    corr_matrix = data[col_names].corr()

    # Correlation Matrix Heatmap
    f, ax = plt.subplots(figsize=(20, 12))
    hm = sns.heatmap(
        round(corr_matrix, 2),
        annot=True,
        ax=ax,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.05,
    )

    bottom, top = ax.get_ylim()
    ax.set_ylim(bottom + 0.5, top - 0.5)

    f.subplots_adjust(top=0.94)
    t = f.suptitle("Correlation Heatmap", fontsize=20)
    plt.show()


def plot_scatter(data, col_x, col_y, hue, title):
    g = sns.lmplot(x=col_x, y=col_y, data=data, hue=hue)
    g.fig.set_figwidth(25)
    g.fig.set_figheight(6)
    plt.title(title, fontsize=30)
    plt.show()


def plot_custom_scatter(data, col_x, col_y, hue, groupby=None):
    sns.set(color_codes=True)

    if groupby:
        for i in data[groupby].unique():
            plot_scatter(data[data[groupby] == i], col_x, col_y, hue, i)
    else:
        plot_scatter(data, col_x, col_y, hue, "Wrocław")


def compare_predictions_with_real(model, X_test, y_test):
    predictions = model.predict(X_test)
    plt.figure(figsize=(20, 5))
    plt.plot(predictions, y_test, ".")

    ticks = np.arange(0, max(y_test.values) + 1, 500)
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.title("Wykres predykcji vs wartości rzeczywistych", fontsize=25)
    plt.xlabel("predykcje", fontsize=15)
    plt.ylabel("Wartości rzeczywiste", fontsize=15)
    plt.plot(ticks, ticks)
    plt.show()


def my_residual_plot(X_train, y_train, X_test, y_test):
    plt.figure(figsize=(20, 5))
    plt.grid(True)

    visualizer = ResidualsPlot(LinearRegression(), hist=False)

    visualizer.fit(X_train, y_train)  # Fit the training data to the visualizer
    visualizer.score(X_test, y_test)  # Evaluate the model on the test data

    ticks = np.arange(1000, max(y_test.values) + 1, 500)

    plt.title("Wykres rezyduów", fontsize=25)
    plt.xlabel("Ceny mieszkań", fontsize=15)
    plt.ylabel("Rezydua", fontsize=15)

    plt.plot(ticks, np.zeros(len(ticks)), "r")
    plt.legend()
    plt.show()


def plot_feature_importance(model_feature_importances, X_train):
    feature_importances = pd.DataFrame(
        model_feature_importances, index=X_train.columns, columns=["importance"]
    ).sort_values("importance", ascending=False)
    plt.figure(figsize=(25, 8))
    feature_importances["importance"].plot(kind="bar")
    plt.ylabel("importance")
    plt.xlabel("feature")
    plt.title(
        "Importances of different variables affecting the magnitude of a scalar coupling constant"
    )

    plt.show()


def interactive_regression_tree(X_train, y_train):
    def plot_regression_tree(crit, split, depth, min_split, min_leaf):
        estimator = DecisionTreeRegressor(
            random_state=0,
            criterion=crit,
            splitter=split,
            max_depth=depth,
            min_samples_split=min_split,
            min_samples_leaf=min_leaf,
        )

        estimator.fit(X_train, y_train)

        graph = Source(
            export_graphviz(
                estimator,
                out_file=None,
                feature_names=list(X_train.columns),
                filled=True,
                rounded=True,
                impurity=False,
            )
        )

        display(SVG(graph.pipe(format="svg")))

        return estimator

    inter = interactive(
        plot_regression_tree,
        crit=["mse", "mae", "friedman_mse"],
        split=["best", "random"],
        depth=[1, 2, 3, 4, 5, 6],
        min_split=(0.1, 1),
        min_leaf=(0.1, 0.5),
    )

    display(inter)


def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    """
    Function plotting precision and recall curve. The independent variables is 
    threshold nd the dependent variables are precision and recall.

    :param numpy.ndarray precisions: Array of precisions for model's predictions.
    :param numpy.ndarray recalls: Array of recalls for model's predictions.
    :param numpy.ndarray thresholds: Array of thresholds for model's predictions.
    """

    plt.figure(figsize=(15, 8))
    plt.grid(False)
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall")
    plt.xlabel("Threshold")
    plt.legend(loc="best")
    plt.ylim([0, 1])
    plt.title("Precision and Recall vs Threshold")
    plt.show()


def plot_pr_curve(recalls, precisions):
    plt.figure(figsize=(15, 8))
    plt.grid(False)
    plt.fill_between(recalls, 0, precisions, alpha=0.2, color="b")
    plt.plot(recalls, precisions)
    
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title("Precision-Recall curve")
    plt.show()


def plot_roc_curve(fpr, tpr):
    """
    Function plotting ROC curve. The independent variables is 
    False positive rate and the dependent variables is True positive rate.

    :param numpy.ndarray fpr: Array of False positives rates
    :param numpy.ndarray tpr: Array of True positives rates.
    """

    plt.figure(figsize=(15, 8))
    plt.grid(False)
    plt.plot(fpr, tpr, "b-", label="ROC curve")
    plt.plot([0, 1], [0, 1], "r--")
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.legend(loc="best")
    plt.ylim([0, 1])
    plt.title("ROC Curve")
    plt.show()


def plot_confusion_matrix(
    cm, classes, normalize=False, title="Confusion matrix", cmap=plt.cm.Blues
):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting 'normalize=True'
    """
    ax, fig = plt.subplots(figsize=(15, 8))
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)

    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    
    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print("Confusion matrix, without normalization")
    print(cm)

    tresh = cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            round(j, 2),
            round(i, 2),
            round(cm[i, j], 2),
            fontsize=25,
            horizontalalignment="center",
            color="magenta" if cm[i, j] > tresh else "black",
        )

    ax = plt.gca()  # only to illustrate what `ax` is

    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.grid(False)
    plt.show()


def plot_example_confusion_matrix(path, size=(13, 10)):
    plt.figure(figsize=size)
    plt.grid(False)
    plt.imshow(plt.imread(path))
