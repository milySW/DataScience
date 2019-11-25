
from sklearn.preprocessing import StandardScaler

def scale_data(data):
    scaled_data = data.copy()

    col_names = list(data.columns.values)
    col_names.pop()

    features = scaled_data[col_names]
    scaler = StandardScaler().fit(features.values)
    features = scaler.transform(features.values)

    scaled_data[col_names] = features
    
    return scaled_data
