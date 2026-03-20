from __future__ import annotations
 
from abc import ABC, abstractmethod
 
import pandas as pd
 
 
class ExportPort(ABC):
    @abstractmethod
    def export_text(self, filename_prefix: str, text: str) -> str:
        raise NotImplementedError
 
    @abstractmethod
    def export_csv(self, df: pd.DataFrame, filename_prefix: str) -> str:
        raise NotImplementedError
 
    @abstractmethod
    def export_excel(self, df: pd.DataFrame, filename_prefix: str) -> str:
        raise NotImplementedError