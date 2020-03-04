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


def encode_implement_all(df, list_of_columns):
    """The functions takes as arguments the df containing the columns to encode 
    and a list of df columns (pandas series) to encode"""
    list_of_columns_to_encode = [df[i] for i in list_of_columns]
    for column in list_of_columns_to_encode:
        encode_and_implement_in_df(df, column)
    for i in list_of_columns_to_encode:
        try:
            del df[str(i.name)]

        except Exception:
            pass

    try:
        del df[float("Nan")]

    except Exception:
        pass

    return df
