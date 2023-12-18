from abc import ABC, abstractmethod
from typing import Any
import pandas as pd


class BaseEntity(ABC):
    @abstractmethod
    def __init__(self, series: pd.Series):
        raise NotImplementedError("Subclasses must implement this method")

    def __eq__(self, other):
        return self.check_is_same_instance(other=other)

    @abstractmethod
    def check_is_same_instance(self, other: Any) -> bool:
        raise NotImplementedError("Subclasses must implement this method")
