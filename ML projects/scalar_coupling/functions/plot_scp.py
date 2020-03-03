import numpy as np
import networkx as nx
import seaborn as sns
import pandas as pd

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from functions.confidence_interval import confidence_interval


def plot_histograms(data, groupby, col_name, xlabel="X"):
    var = 1
    fig = plt.figure(figsize=(24, 8))

    for i in data[groupby].unique():
        plt.subplot(2, 4, var)
        plt.hist(
            data[data[groupby] == i][col_name],
            bins=30,
            color=list(np.random.choice(range(256), size=3) / 256),
            edgecolor="black",
            linewidth=0.5,
            density=True,
        )
        plt.xlabel(xlabel)
        plt.ylabel("Probability")
        plt.title(col_name + "distribuition for " + i + " type")
        var += 1
    plt.tight_layout()


def plot_bars(col, col_name):
    fig = plt.figure(figsize=(20, 6))
    performance = [list(col).count(i) for i in col.unique()]
    color = [list(np.random.choice(range(256), size=3) / 256) for _ in col.unique()]
    plt.bar(col.unique(), performance, align="center", color=color, edgecolor="black")
    plt.ylabel("Quantity")
    plt.xlabel("Indices")
    plt.title("Number of idices in " + col_name)


def plot_graph(data, groupby, source, target, edge_attr):
    fig, ax = plt.subplots(figsize=(20, 12))

    indices_0 = confidence_interval(data[source])
    indices_1 = confidence_interval(data[target])

    for i, t in enumerate(data[groupby].unique()):
        data_type = data[data[groupby] == t]
        data_type = data_type[
            (data_type[source].isin(indices_0)) & (data_type[target].isin(indices_1))
        ]
        G = nx.from_pandas_edgelist(data_type, source, target, [edge_attr])
        plt.subplot(2, 4, i + 1)
        nx.draw(G, with_labels=True)
        plt.title(f"Graph for type {t}")


# Correlation Matrix Heatmap
def plot_corr_matrix(data, title):
    corr_matrix = data.corr()
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
    t = f.suptitle(title, fontsize=20)


def plot_3d_atoms(data, list_of_cordinates, groupby, individual=False):
    """
    The function draws 3d scatter graphs for one or many atoms.

    :param list list_of_atoms - list of atoms for which we draw a plot.
    :param individual - variable determining whether the graphs for individual 
    atoms should appear on each other or on separate plots.
    """
    atoms = data[groupby].value_counts().index
    colors = ["r", "g", "b", "k", "m"]
    atom_colors_dict = dict(zip(atoms, colors))

    axes = [-1.8, 1.8, -1.3, 1.3, -1.0, 1.0]

    x1s = np.linspace(axes[0], axes[1], 10)
    x2s = np.linspace(axes[2], axes[3], 10)
    x1, x2 = np.meshgrid(x1s, x2s)

    fig = plt.figure(figsize=(30, 8))
    if not individual:
        ax = fig.add_subplot(111, projection="3d")
        surf = ax.plot_surface(x1, x2, x1, alpha=0.2, color="k")
        ax.plot([0], [0], [0], "k.")

    counter = 1
    for i in atom_colors_dict.keys():
        if individual:
            ax = fig.add_subplot(
                1, len(atom_colors_dict.keys()), counter, projection="3d"
            )
            surf = ax.plot_surface(x1, x2, x1, alpha=0.2, color="k")
            ax.plot([0], [0], [0], "k.")
            counter += 1

        ax.plot(
            data[data[groupby] == i][list_of_cordinates].values[:, 0],
            data[data[groupby] == i][list_of_cordinates].values[:, 1],
            data[data[groupby] == i][list_of_cordinates].values[:, 2],
            atom_colors_dict[i] + ".",
            alpha=0.75,
            label=i,
        )

        surf._facecolors2d = surf._facecolors3d
        surf._edgecolors2d = surf._edgecolors3d

        ax.legend(loc="upper right")

    ax.set_xlabel("$X$", fontsize=18)
    ax.set_ylabel("$Y$", fontsize=18)
    ax.set_zlabel("$Z$", fontsize=18)

    ax.set_xlim(
        int(min(data[list_of_cordinates].values[:, 0])),
        int(max(data[list_of_cordinates].values[:, 0])),
    )
    ax.set_ylim(
        int(min(data[list_of_cordinates].values[:, 1])),
        int(max(data[list_of_cordinates].values[:, 1])),
    )
    ax.set_zlim(
        int(min(data[list_of_cordinates].values[:, 2])),
        int(max(data[list_of_cordinates].values[:, 2])),
    )

    plt.show()


def plot_oof_preds(types, lims, y_train, my_dict, type_list):
    plot_data = pd.DataFrame(y_train)
    plot_data.index.name = "id"
    plot_data["yhat"] = my_dict["oof"]
    plot_data["type"] = type_list

    for i, ctype in enumerate(types):
        plt.figure(figsize=(6, 6))
        sns.scatterplot(
            x="scalar_coupling_constant",
            y="yhat",
            data=plot_data.loc[
                plot_data["type"] == ctype, ["scalar_coupling_constant", "yhat"]
            ],
        )

        plt.xlim((lims[i][0], lims[i][1]))
        plt.ylim((lims[i][0], lims[i][1]))
        plt.plot([lims[i][0], lims[i][1]], [lims[i][0], lims[i][1]])
        plt.xlabel("scalar_coupling_constant")
        plt.ylabel("predicted")
        plt.title(f"{ctype}", fontsize=18)
        plt.show()
