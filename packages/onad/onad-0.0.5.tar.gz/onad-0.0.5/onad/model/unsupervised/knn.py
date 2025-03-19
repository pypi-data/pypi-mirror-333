from typing import Dict
from onad.base.model import BaseModel
from onad.base.similarity import BaseSimilaritySearchEngine


class KNN(BaseModel):
    """
    K-Nearest Neighbors (KNN) model for similarity-based machine learning.

    This class implements a KNN algorithm that relies on a similarity search engine
    to find the nearest neighbors of a given resources point. It inherits from `BaseModel`
    and is designed to work with feature vectors represented as dictionaries.

    Attributes:
        k (int): The number of nearest neighbors to consider.
        engine (BaseSimilaritySearchEngine): The similarity search engine used to find neighbors.
    """

    def __init__(self, k: int, similarity_engine: BaseSimilaritySearchEngine):
        """
        Initializes the KNN model with the specified number of neighbors and similarity engine.

        Args:
            k (int): The number of nearest neighbors to consider.
            similarity_engine (BaseSimilaritySearchEngine): An instance of a similarity search engine
                that will be used to compute nearest neighbors.
        """
        self.k: int = k
        self.engine: BaseSimilaritySearchEngine = similarity_engine

    def learn_one(self, x: Dict[str, float]) -> None:
        """
        Adds a new resources point to the model for future similarity searches.

        Args:
            x (Dict[str, float]): A dictionary representing a resources point, where keys are feature names
                and values are feature values.
        """
        self.engine.append(x)

    def score_one(self, x: Dict[str, float]) -> float:
        """
        Computes a score for the given resources point based on its nearest neighbors.

        Args:
            x (Dict[str, float]): A dictionary representing a resources point, where keys are feature names
                and values are feature values.

        Returns:
            float: A score representing the similarity of the resources point to its nearest neighbors.
                The exact interpretation of the score depends on the underlying similarity engine.
        """
        return self.engine.search(x, n_neighbors=self.k)
