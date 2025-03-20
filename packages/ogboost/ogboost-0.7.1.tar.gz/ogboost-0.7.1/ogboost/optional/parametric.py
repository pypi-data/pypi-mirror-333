from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np
from statsmodels.miscmodels.ordinal_model import OrderedModel
from ogboost.main import concordance_index

class StatsModelsOrderedModel(BaseEstimator, ClassifierMixin):
    """
    A basic scikit-learn wrapper for statsmodels' OrderedModel (linear ordinal regression).

    This wrapper adapts the OrderedModel to the scikit-learn API, allowing it to be used
    with standard model selection tools such as cross_val_score.

    Parameters
    ----------
    distr : str, default='probit'
        The distribution used in the OrderedModel (e.g., 'probit' or 'logit').
    fit_method : str, default='bfgs'
        The optimization method to use when fitting the model.
    fit_disp : bool, default=False
        Whether to display convergence messages during fitting.
    fit_maxiter : int, default=500
        The maximum number of iterations to use during fitting.
    
    Attributes
    ----------
    model_ : OrderedModel instance
        The underlying OrderedModel created during fit.
    res_ : Results instance
        The fitted results from OrderedModel.
    """
    def __init__(self, distr='probit', fit_method='bfgs', fit_disp=False, fit_maxiter=500):
        self.distr = distr
        self.fit_method = fit_method
        self.fit_disp = fit_disp
        self.fit_maxiter = fit_maxiter

    def fit(self, X, y):
        """
        Fit the ordered model using the provided training data.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Ordinal target values.
        
        Returns
        -------
        self : object
            Returns self.
        """
        self.model_ = OrderedModel(y, X, distr=self.distr)
        self.res_ = self.model_.fit(method=self.fit_method, disp=self.fit_disp, maxiter=self.fit_maxiter)
        return self

    def predict_proba(self, X):
        """
        Predict class probabilities for X.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data.
        
        Returns
        -------
        probas : ndarray of shape (n_samples, n_classes)
            The predicted class probabilities.
        """
        return self.model_.predict(self.res_.params, X)

    def decision_function(self, X):
        """
        Compute the latent function (linear predictor) for X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data.

        Returns
        -------
        latent_scores : ndarray of shape (n_samples,)
            The latent function values.
        """
        return self.model_.predict(self.res_.params, X, which='linpred')

    def predict(self, X):
        """
        Predict class labels for X by selecting the class with the highest probability.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data.
        
        Returns
        -------
        labels : ndarray of shape (n_samples,)
            Predicted ordinal class labels.
        """
        probas = self.predict_proba(X)
        return np.argmax(probas, axis=1)

    def score(self, X, y, sample_weight=None):
        """
        Compute the performance of the model using the concordance index on the latent scores.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input data.
        y : array-like of shape (n_samples,)
            True ordinal labels.
        sample_weight : array-like, optional
            Sample weights for each observation.
        
        Returns
        -------
        score : float
            The concordance index computed on the latent function values.
        """
        latent_scores = self.decision_function(X)
        return concordance_index(y, latent_scores, sample_weight=sample_weight)
