def confidence_interval(col, alfa=0.01):
    interval = list(
        col.value_counts(normalize=True)[col.value_counts(normalize=True) >= alfa].index
    )
    return interval
