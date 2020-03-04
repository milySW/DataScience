from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import make_scorer, fbeta_score


def prepare_model(clf, param_grid, X_train, y_train, score_type):
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
    If None every column is used.
    
    :returns: 
        - imblearn.pipeline.Pipeline best -  best model after fitting the data.
        - dict grid.best_params_ - Dictionary with best params.
        - imblearn.pipeline.Pipeline grid.best_estimator_ - best model before fitting the data.
        than the training on selected columns
    """
        
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
        
    return best, grid.best_params_, grid.best_estimator_
