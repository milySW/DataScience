import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import seaborn as sns
import itertools

from mpl_toolkits.mplot3d import Axes3D


def plot_correlations(correlations):
    f = plt.figure(figsize=(20,5))
    ax = f.add_subplot(1,1,1)
    plt.bar(correlations.index, correlations)
    for i in range(len(correlations)):
        if correlations[i] < 0:
            ax.get_children()[i].set_color('r')
    plt.xticks(rotation=45)
    plt.title('Correlations with label column', fontsize=20)
    plt.show()


# Correlation Matrix Heatmap
def correlation_heatmap(corr_matrix):
    f, ax = plt.subplots(figsize=(20, 12))
    hm = sns.heatmap(round(corr_matrix,2), annot=True, ax=ax, cmap="coolwarm",fmt='.2f',
                     linewidths=.05)

    bottom, top = ax.get_ylim()
    ax.set_ylim(bottom + 0.5, top - 0.5)

    f.subplots_adjust(top=0.94)
    t= f.suptitle('Fraud Detection Correlation Heatmap', fontsize=20)
    plt.show()


def generate_grid_set(axes=[-1.8, 1.8, -1.3, 1.3, -1.0, 1.0], n=10):
    x1s = np.linspace(axes[0], axes[1], n)
    x2s = np.linspace(axes[2], axes[3], n)
    x1, x2 = np.meshgrid(x1s, x2s)
    return x1, x2
    

def plot_2d_scatter(X_train, y_train, column_x, column_y, column_x_name, column_y_name):
    fig = plt.figure(figsize=(15, 5))
    ax = fig.add_subplot(111)


    index_0 = [not (i-1) for i in y_train.values]
    index_1 = [not i for i in index_0]

    ax.plot(X_train[[column_x, column_y]].values[index_0, 0], X_train[[column_x, column_y]].values[index_0, 1], "k+")

    ax.plot(X_train[[column_x, column_y]].values[index_1, 0], X_train[[column_x, column_y]].values[index_1, 1], "r.")

    ax.set_xlabel(column_x_name, fontsize=18)
    ax.set_ylabel(column_y_name, fontsize=18, rotation=0)
    ax.axis([min(X_train[[column_x, column_y]].values[:, 0]) - 2, max(X_train[[column_x, column_y]].values[:, 0]) + 2
             , min(X_train[[column_x, column_y]].values[:, 1]) - 2, max(X_train[[column_x, column_y]].values[:, 1]) + 2])
    ax.grid(True)
    plt.show()

def plot_3d_scatter(X_train, y_train, column_x, column_y,  column_z, column_x_name, column_y_name,  column_z_name):
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection='3d')

    index_0 = [not (i-1) for i in y_train.values]
    index_1 = [not i for i in index_0]

    x1, x2 = generate_grid_set()
    ax.plot_surface(x1, x2, x1, alpha=0.2, color="k")

    ax.plot([0], [0], [0], "k.")


    ax.plot(X_train[[column_x, column_y,  column_z]].values[index_0, 0], X_train[[column_x, column_y,  column_z]].values[index_0, 1], X_train[[column_x, column_y,  column_z]].values[index_0, 2], "k+")
    ax.plot(X_train[[column_x, column_y,  column_z]].values[index_0, 0], X_train[[column_x, column_y,  column_z]].values[index_0, 1], X_train[[column_x, column_y,  column_z]].values[index_0, 2], "k.")

    ax.plot(X_train[[column_x, column_y,  column_z]].values[index_1, 0], X_train[[column_x, column_y,  column_z]].values[index_1, 1], X_train[[column_x, column_y,  column_z]].values[index_1, 2], "r+")
    ax.plot(X_train[[column_x, column_y,  column_z]].values[index_1, 0], X_train[[column_x, column_y,  column_z]].values[index_1, 1], X_train[[column_x, column_y,  column_z]].values[index_1, 2], "r.")

    ax.set_xlabel(column_x_name, fontsize=18)
    ax.set_ylabel(column_y_name, fontsize=18)
    ax.set_zlabel(column_z_name, fontsize=18)

    ax.set_xlim(int(min(X_train[[column_x, column_y,  column_z]].values[:, 0])), int(max(X_train[[column_x, column_y,  column_z]].values[:, 0])))
    ax.set_ylim(int(min(X_train[[column_x, column_y,  column_z]].values[:, 1])), int(max(X_train[[column_x, column_y,  column_z]].values[:, 1])))
    ax.set_zlim(int(min(X_train[[column_x, column_y,  column_z]].values[:, 2])), int(max(X_train[[column_x, column_y,  column_z]].values[:, 2])))

    plt.show()


def plot_density(data_train, col_names):
    fig = plt.figure(figsize = (20, 20))
    ax = fig.gca()
    
    fraud_hist_data = data_train[data_train['Class'] == 1][col_names]
    clients_hist_data = data_train[data_train['Class'] == 0][col_names]

    for num, col in enumerate(col_names):
        plt.subplot(6, 5, num + 1)

        min_x = min(clients_hist_data[col])
        max_x = max(clients_hist_data[col])
        one_bar = (max_x-min_x)/20
        min_x = min_x + one_bar/2
        max_x = max_x - one_bar/2 + 0.010
        bins = list(np.arange(min_x, max_x, one_bar))

        sns.kdeplot(clients_hist_data[col], shade=True, label='Client');
        sns.kdeplot(fraud_hist_data[col], shade=True, label='Fraud');
        plt.title(col)
        
    plt.tight_layout(rect=(0, 0, 1.2, 1.2))
    plt.show()


def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting 'normalize=True'
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print('Normalized confusion matrix')
    else:
        print('Confusion matrix, without normalization')
    print(cm)
    
    tresh = cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(round(j, 2), round(i, 2), round(cm[i, j], 2), horizontalalignment='center', color='magenta' if cm[i, j] > tresh else 'black')
    
    ax = plt.gca()  # only to illustrate what `ax` is
    ax.autoscale(enable=True, axis='y', tight=False)
    
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()


def plot_roc_curve(fpr, tpr):
    """
    Function plotting ROC curve. The independent variables is 
    False positive rate and the dependent variables is True positive rate.

    :param numpy.ndarray fpr: Array of False positives rates
    :param numpy.ndarray tpr: Array of True positives rates.
    """
    
    plt.plot(fpr, tpr, "b-", label="ROC curve")
    plt.plot([0, 1], [0,1], "r--")
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.legend(loc="best")
    plt.ylim([0, 1])
    plt.title('ROC Curve')
    plt.show()


def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    """
    Function plotting precision and recall curve. The independent variables is 
    threshold nd the dependent variables are precision and recall.

    :param numpy.ndarray precisions: Array of precisions for model's predictions.
    :param numpy.ndarray recalls: Array of recalls for model's predictions.
    :param numpy.ndarray thresholds: Array of thresholds for model's predictions.
    """
    
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall")
    plt.xlabel("Threshold")
    plt.legend(loc="best")
    plt.ylim([0, 1])
    plt.title('Precision and Recall vs Threshold')
    plt.show()


def plot_pr_curve(recalls, precisions):
    plt.fill_between(recalls, 0, precisions, alpha=0.2, color='b')
    plt.plot(recalls, precisions)

    plt.xlabel("Recall")
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('Precision-Recall curve')
    plt.show()
