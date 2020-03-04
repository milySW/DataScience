from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    roc_auc_score,
    fbeta_score
)


def model_tests(model, X_test, y_test, mode=2, from_grid=True):
    """
    Function printing info about model performance on test set.

    :param model: sklearn model before fitting.
    :param pandas.core.frame.DataFrame: Test data instances.
    :param pandas.core.frame.DataFrame: Label for test data instances.
    :param int mode: if mode=1 model_tests show you report without classification_report
    """
    if from_grid:
        predictions = model[0].predict(X_test)
        print('Best params: \t', model[1])
        print('')
    else:
        predictions = model.predict(X_test)
    
    print('Precision score: \t', precision_score(y_test, predictions))
    print('Recall score: \t', recall_score(y_test, predictions))
    print('F1 score: \t', f1_score(y_test, predictions))
    print('F_beta score: \t', fbeta_score(y_test, predictions, 2**(1/2)))
    print('')
    print('Roc AUC Score: \t', roc_auc_score(y_test, predictions))
    
    if mode==2:
        print('')
        print(classification_report(y_test, predictions, target_names=['Not Sold', 'Sold']))

