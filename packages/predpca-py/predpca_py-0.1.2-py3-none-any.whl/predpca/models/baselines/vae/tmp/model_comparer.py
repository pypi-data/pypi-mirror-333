import numpy as np
from sklearn.base import BaseEstimator

from predpca.models.base_encoder import BaseEncoder
from predpca.models.wta_classifier import ICAWTAClassifier


class ModelComparer:
    """Class for comparing different models using the same evaluation metrics"""

    def __init__(
        self,
        models: dict[str, BaseEncoder],
        classifier: BaseEstimator | None = None,
    ):
        """
        Args:
            models: Dictionary of model name to model instance
            classifier: Classifier to use for evaluation. If None, uses ICAWTAClassifier
        """
        self.models = models
        self.classifier = classifier or ICAWTAClassifier()
        self.results: dict[str, dict[str, float]] = {}

    def fit_and_evaluate(
        self,
        X_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
    ) -> dict[str, dict[str, float]]:
        """Fit all models and evaluate them using the same metrics

        Args:
            X_train: Training data (n_features, n_samples)
            X_test: Test data (n_features, n_samples)
            y_test: Test labels (n_samples,)

        Returns:
            Dictionary of model names to their evaluation metrics
        """
        self.results = {}

        for name, model in self.models.items():
            print(f"Evaluating {name}...")

            # Train the model
            model.fit(X_train)

            # Get encodings
            train_encodings = model.transform(X_train)
            test_encodings = model.transform(X_test)

            # Train classifier
            self.classifier.fit(train_encodings)

            # Evaluate
            metrics = model.evaluate(X_test, y_test, self.classifier)
            self.results[name] = metrics

        return self.results

    def print_results(self):
        """Print the comparison results in a formatted way"""
        if not self.results:
            print("No results available. Run fit_and_evaluate first.")
            return

        for model_name, metrics in self.results.items():
            print(f"\nResults for {model_name}:")
            for metric_name, value in metrics.items():
                print(f"{metric_name}: {value:.4f}")
