from abc import ABC, abstractmethod
import numpy as np


class Normalizer(ABC):

    def __init__(self):
        pass

    def calibrate(
        self, generation_performance_scores: list, truth_values: list
    ):  # -1 means invalid performance score, remove nan values from truth_values
        pos_inf_replacement = 1e10
        neg_inf_replacement = -1e10
        generation_performance_scores = np.array(generation_performance_scores)
        truth_values = np.array(truth_values)
        truth_values = truth_values[generation_performance_scores != -1]
        generation_performance_scores = generation_performance_scores[
            generation_performance_scores != -1
        ]
        truth_values[np.isnan(truth_values)] = 0.0
        truth_values[truth_values == np.inf] = pos_inf_replacement
        truth_values[truth_values == -np.inf] = neg_inf_replacement

        self.fit(
            generation_performance_scores=generation_performance_scores,
            truth_values=truth_values,
        )

    def __call__(self, truth_value: float):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def fit(self, generation_performance_scores: list, truth_values: list):
        raise NotImplementedError("Subclasses must implement this method")

    # @abstractmethod
    # def transform(self, truth_values:list):
    #     raise NotImplementedError("Subclasses must implement this method")

    def __str__(self):
        return f"{self.__class__.__name__} with {str(self.__dict__)}"
