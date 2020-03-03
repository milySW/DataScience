import numpy as np
import pandas as pd

from functions.confidence_interval import confidence_interval


def add_number_of_edges(
    data, groupby="type", source="atom_index_0", target="atom_index_1"
):
    empty_column = np.zeros(len(data))
    data["connections_0"] = empty_column
    data["connections_1"] = empty_column

    list_of_indices = set(list(data[source]) + list(data[target]))

    indices_0 = confidence_interval(data[source])
    indices_1 = confidence_interval(data[target])

    for i, t in enumerate(data[groupby].unique()):
        data_type = data[data[groupby] == t]
        data_type = data_type[
            (data_type[source].isin(indices_0)) & (data_type[target].isin(indices_1))
        ]
        data_type["connection"] = data_type[[source, target]].apply(
            lambda x: " ".join(x.astype(str)), axis=1
        )

        unique_connections = data_type["connection"].unique()
        for j in list_of_indices:
            connections = sum(map(lambda x: str(j) in x.split(" "), unique_connections))
            data.loc[
                (data[groupby] == t) & (data[source] == j), "connections_0"
            ] = connections
            data.loc[
                (data[groupby] == t) & (data[target] == j), "connections_1"
            ] = connections
    return data


def map_atom_info(df, df_with_cordinates, list_atom_idx):
    for atom_idx in list_atom_idx:
        df = pd.merge(
            df,
            df_with_cordinates,
            how="left",
            left_on=["molecule_name", f"atom_index_{atom_idx}"],
            right_on=["molecule_name", "atom_index"],
        )

        df = df.drop("atom_index", axis=1)
        df = df.rename(
            columns={
                "atom": f"atom_{atom_idx}",
                "x": f"x_{atom_idx}",
                "y": f"y_{atom_idx}",
                "z": f"z_{atom_idx}",
            }
        )
    return df


def add_distances(data, start_points, end_points):
    data_p_0 = data[start_points].values
    data_p_1 = data[end_points].values

    data["dist"] = np.linalg.norm(data_p_0 - data_p_1, axis=1)
    for i in range(len(start_points)):
        dim = start_points[i][0]
        data["dist_" + dim] = (data[start_points[i]] - data[end_points[i]]) ** 2
    return data


def add_type_info(data, col_to_split):
    data["type_0"] = data[col_to_split].apply(lambda x: x[0])
    data["type_1"] = data[col_to_split].apply(lambda x: x[1:])
    return data


def add_mean_dist(data, groupby_list):
    for i in groupby_list:
        if type(i) != list:
            name = i
        elif type(i) == list:
            name = "_".join(i)
        data["dist_to_" + name + "_mean"] = data["dist"] / data.groupby(i)[
            "dist"
        ].transform("mean")
    return data


def one_hot_encoder(df_column, what_is_1):
    output = []
    for row in df_column:
        if row == what_is_1:
            output.append(1)
        else:
            output.append(0)
    return output


def one_hot_caller(df_column, set_of_categories):
    cat_columns_encoded = {}
    for thing in set_of_categories:
        cat_columns_encoded[thing] = one_hot_encoder(df_column, thing)
    return cat_columns_encoded


def get_distinct_values_from_column(df_column):
    distinct_df_column = list(set([row for row in df_column]))
    return distinct_df_column


def call_one_hot_caller(df_column):
    distinct = get_distinct_values_from_column(df_column=df_column)
    return one_hot_caller(df_column, distinct)


def encode_and_implement_in_df(df, df_column):
    for key, value in call_one_hot_caller(df_column).items():
        df[key] = value
    return df


def encode_implement_all(df, list_of_columns_to_encode):
    """The functions takes as arguments the df containing the columns to encode 
    and a list of df columns (pandas series) to encode"""
    df_with_columns_to_encode = df[list_of_columns_to_encode]
    for column in df_with_columns_to_encode.columns:
        encode_and_implement_in_df(df, df_with_columns_to_encode[column])
    for i in df_with_columns_to_encode.columns:
        try:
            del df[i]

        except Exception:
            pass

    return df
