import matplotlib.pyplot as plt
import matplotlib.image as img
from PIL import Image
import numpy as np
import itertools


def plot_accuracy_loss(history):
    """
    Function plotting:
    :accuracy and validation accuracy on firs plot
    :loss and validation loss on second plot
    """
    fig = plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(history.history["accuracy"])
    plt.plot(history.history["val_accuracy"])
    plt.title("model accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    plt.legend(["train", "validation"], loc="upper left")
    plt.ylim([0, 1])

    plt.subplot(1, 2, 2)
    plt.plot(history.history["loss"])
    plt.plot(history.history["val_loss"])
    plt.title("model loss")
    plt.ylabel("loss")
    plt.xlabel("epoch")
    plt.legend(["train", "test"], loc="upper right")
    plt.show()


def plot_predictions_or_examples(
    filenames,
    preds=None,
    title="Predictions from test set",
    root_dir="data_food_classifier_MG",
):
    """
    Method plotting test set with predictions or example
    images from directory when preds are not given.
    
    :param preds - list of predictions for test set.
    :param filenames - list of filenames in test set.

    :return names of wrong predicted files.
    """
    root_listdir = filenames[:60]
    if preds:
        preds = preds[:60]

    fig, ax = plt.subplots(10, 6, frameon=False, figsize=(15, 25))
    fig.suptitle(title, fontsize=20)

    row = 0
    col = 0

    wrong_prediction_filenames = []
    ec = (0, 0.6, 0.1)
    fc = (0, 0.7, 0.2)
    for i, element in enumerate(root_listdir):
        try:
            if preds:
                if "slow_food" in element:
                    last_dir = "slow_food"
                    class_number = 0
                else:
                    last_dir = "fast_food"
                    class_number = 1

                if preds[i] == 0:
                    class_name = "slow food"
                else:
                    class_name = "fast food"

                if class_number != preds[i]:
                    fc = (1, 0.0, 0.0)
                    wrong_prediction_filenames.append(element)
                else:
                    fc = (0, 0.7, 0.2)

                image = Image.open(root_dir + "/test/" + last_dir + "/" + element)

            else:
                if "slow_food" in element:
                    class_name = "slow food"
                else:
                    class_name = "fast food"
                image = Image.open(root_dir + "/" + element)

            image = image.resize((120, 120), Image.ANTIALIAS)
            ax[row][col].imshow(image)

            ax[row][col].text(
                0,
                -20,
                class_name,
                size=10,
                rotation=0,
                ha="left",
                va="top",
                bbox=dict(boxstyle="round", ec=ec, fc=fc),
            )

            ax[row][col].set_xticks([])
            ax[row][col].set_yticks([])

            col += 1
            if col % 6 == 0 and col * row != 54:
                col = 0
                row += 1
            elif col * row == 54:
                break
        except (OSError, ValueError) as e:
            print(e)
    if preds:
        return wrong_prediction_filenames


def plot_confusion_matrix(
    cm, classes, normalize=False, title="Confusion matrix", cmap=plt.cm.Blues
):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting 'normalize=True'
    """
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
            horizontalalignment="center",
            color="white" if cm[i, j] > tresh else "black",
        )

    ax = plt.gca()  # only to illustrate what `ax` is
    ax.autoscale(enable=True, axis="y", tight=False)

    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel("Predicted label")
