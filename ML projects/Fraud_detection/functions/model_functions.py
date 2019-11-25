from sklearn.model_selection import GridSearchCV
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report, roc_auc_score, make_scorer, fbeta_score
from sklearn.pipeline import Pipeline
from sklearn.metrics import make_scorer, fbeta_score

f2_score = make_scorer(fbeta_score, beta=2**(1/2), pos_label=-1)

def prepare_model(clf, param_grid, X_train, y_train, score_type=f2_score, list_of_selected_columns=None):
    """
    Function use GridSearch to find best model hyperparameters and decide 
    if using all columns or only the most important ones will train the 
    best model.
    
    :param clf: sklearn model with base class - BaseEstimator.
    
    :param dict param_grid: Dictionary with parameters names (string) 
    as keys and lists of parameter settings to try as values, 
    or a list of such dictionaries, in which case the grids spanned 
    by each dictionary in the list are explored. 
    This enables searching over any sequence of parameter settings.
    
    :param pandas.core.frame.DataFrame X_train: Traininig data instances.
    :param pandas.core.frame.DataFrame y_train: Labels for traininig data instances.
    :param str score_type: type of scoring during GridSearch
    :param list list_of_selected_columns: list of columns used during training.
    If None every column is used.
    
    :returns: 
        - imblearn.pipeline.Pipeline best -  best model after fitting the data.
        - dict grid.best_params_ - Dictionary with best params.
        - imblearn.pipeline.Pipeline grid.best_estimator_ - best model before fitting the data.
        - str all_or_selected - information whether the training on all columns was more effective 
        than the training on selected columns
    """
    
    all_or_selected = 'all'
    
    list_of_keys = list(param_grid.keys())
    for old_key in list_of_keys :
        param_grid['clf__' + old_key] = param_grid.pop(old_key)
        
    model = Pipeline([
        ('clf', clf)
    ])

    grid = GridSearchCV(model, param_grid, cv=3, scoring=score_type, verbose=1)
    grid.fit(X_train, y_train)
    
    params = grid.best_params_
    estimator = grid.best_estimator_
    best = estimator.fit(X_train, y_train)
    
    if list_of_selected_columns != None:
        grid_2 = GridSearchCV(model, params, cv=3, scoring=score_type, verbose=1)
        grid_2.fit(X_train[list_of_selected_columns], y_train)
        
        if grid_2.best_score_ > grid.best_score_:
            params = grid_2.best_params_
            estimator = grid_2.best_estimator_
            best = estimator.fit(X_train, y_train)
            all_or_selected = 'selected'
            return best, grid.best_params_, grid.best_estimator_, all_or_selected
        
    return best, grid.best_params_, grid.best_estimator_, all_or_selected


def model_tests(model, X_test, y_test, mode=2, from_grid=True):
    """
    Function printing info about model performance on test set.

    :param model: sklearn model before fitting.
    :param pandas.core.frame.DataFrame: Test data instances.
    :param pandas.core.frame.DataFrame: Label for test data instances.
    :param int mode: if mode=1 model_tests show you report without classification_report
    :param int from_grid: param for checking if our imput is normal or from prepare_model fuction
    """
    if from_grid:
        predictions = model[0].predict(X_test)
        print('Best params: \t', model[1])
        print('')
    else:
        predictions = model.predict(X_test)

    predictions, y_test_original = transform_to_orginal(predictions, y_test.values)
    
    print('Precision score: \t', precision_score(y_test_original, predictions))
    print('Recall score: \t', recall_score(y_test_original, predictions))
    print('F1 score: \t', f1_score(y_test_original, predictions))
    print('F_beta score: \t', fbeta_score(y_test_original, predictions, 2**(1/2)))
    print('')
    print('Roc AUC Score: \t', roc_auc_score(y_test_original, predictions))
    
    if mode==2:
        print('')
        print(classification_report(y_test_original, predictions, target_names=['Client', 'Fraud']))


def transform_to_orginal(predictions, y_test_values):
    predictions = [1 if i == -1 else 0 for i in predictions]
    y_test_original = [1 if i == -1 else 0 for i in y_test_values]
    return predictions, y_test_original
    
