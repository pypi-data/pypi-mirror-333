from abc import ABC, abstractmethod
from typing import Self

import numpy as np


class BaseModelEvaluator(ABC):
    """Abstract class for models with fit/transform interface"""

    @abstractmethod
    def fit(self, X: np.ndarray, y: np.ndarray | None = None) -> Self:
        """Train the model"""
        # TODO: is there any model that requires y?
        pass

    @abstractmethod
    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform the data to latent space

        Args:
            X: (n_samples, n_features)
        Returns:
            encodings: (n_samples, n_features)
        """
        pass
