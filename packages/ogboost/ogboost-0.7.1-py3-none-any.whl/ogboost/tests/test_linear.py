import numpy as np
import pytest
from ogboost import StatsModelsOrderedModel
from ogboost import load_wine_quality  # Import the dataset loader

@pytest.fixture
def dataset():
    """Load the Wine Quality dataset."""
    X, y, _, _ = load_wine_quality(return_X_y=True)
    return X, y

@pytest.fixture
def model():
    """Fixture to create a StatsModelsOrderedModel instance."""
    return StatsModelsOrderedModel(distr='probit', fit_method='bfgs', fit_disp=False, fit_maxiter=250)

def test_initialization(model):
    """Test that the model initializes with the correct parameters."""
    assert model.distr == 'probit'
    assert model.fit_method == 'bfgs'
    assert model.fit_disp is False
    assert model.fit_maxiter == 250

def test_fit_runs_without_error(model, dataset):
    """Test that fit() runs without errors."""
    X, y = dataset
    model.fit(X, y)
    assert model.model_ is not None
    assert model.res_ is not None

def test_predict_proba_output_shape(model, dataset):
    """Test that predict_proba() outputs valid probability distributions."""
    X, y = dataset
    model.fit(X, y)
    probas = model.predict_proba(X[:10])  # Predict on a small subset
    assert probas.shape == (10, len(np.unique(y)))  # n_samples x n_classes
    assert np.all(probas >= 0) and np.all(probas <= 1)  # Probabilities should be between 0 and 1

def test_predict_output_values(model, dataset):
    """Test that predict() outputs valid ordinal labels."""
    X, y = dataset
    model.fit(X, y)
    predictions = model.predict(X[:10])
    assert predictions.shape == (10,)
    assert np.all(np.isin(predictions, np.unique(y)))  # Ensure predicted labels are in the expected range

def test_decision_function_output(model, dataset):
    """Test that decision_function() returns a valid latent score."""
    X, y = dataset
    model.fit(X, y)
    latent_scores = model.decision_function(X[:10])
    assert latent_scores.shape == (10,)
    assert np.issubdtype(latent_scores.dtype, np.floating)  # Should return floating point numbers

def test_score_function(model, dataset):
    """Test that score() runs without error and returns a float."""
    X, y = dataset
    model.fit(X, y)
    score = model.score(X[:10], y[:10])  # Evaluate on a small subset
    assert isinstance(score, float)
