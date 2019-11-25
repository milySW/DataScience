def replace_values_in_column(column, list_of_changes):
    for i in list_of_changes:
        column = column.replace(i[0], i[1])
    return column
