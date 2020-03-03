def column_metrics(column):
    print("Średnia: \t", column.mean())
    print("Wariancja: \t", column.var())
    print("Skośność: \t", column.skew())
    print("Kurtoza: \t", column.kurtosis())
    print("Mediana: \t", column.median())
    print("Mediana: \t", column.median())
    print("Moda: \t \t", float(column.mode()))
