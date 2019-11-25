import os
import numpy as np

from imblearn.combine import SMOTETomek

def resample_data(X_train, y_train):
    if 'X_train_resampled.txt' in os.listdir(os.getcwd() + '/data') and 'y_train_resampled.txt' in os.listdir(os.getcwd() + '/data'):
        X_train_resampled = np.loadtxt('data/X_train_resampled.txt', dtype=float)
        y_train_resampled = np.loadtxt('data/y_train_resampled.txt', dtype=int)

    else:
        smote = SMOTETomek(1/100)
        X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
        np.savetxt('data/X_train_resampled.txt', X_train_resampled, fmt='%f')
        np.savetxt('data/y_train_resampled.txt', y_train_resampled, fmt='%d')

    return X_train_resampled, y_train_resampled
