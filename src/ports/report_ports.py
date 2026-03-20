from __future__ import annotations
 
from typing import Protocol
 
import pandas as pd
 
 
class CarReportPort(Protocol):
    def generate_text_report(self, data: list[dict] | None = None) -> str:
        ...
 
    def generate_dataframe(self, data: list[dict] | None = None) -> pd.DataFrame:
        ...
 
    def get_stats(self, data: list[dict] | None = None) -> tuple[str, str, str, str, str]:
        ...
 

class PartReportPort(Protocol):
    def generate_text_report(self, data: list[dict] | None = None) -> str:
        ...
 
    def generate_dataframe(self, data: list[dict] | None = None) -> pd.DataFrame:
        ...
 
    def get_stats(self, data: list[dict] | None = None) -> tuple[str, str, str, str]:
        ...
 
 
class CustomerReportPort(Protocol):
    def generate_text_report(self, data: list[dict] | None = None) -> str:
        ...
 
    def generate_dataframe(self, data: list[dict] | None = None) -> pd.DataFrame:
        ...
 
    def get_stats(self, data: list[dict] | None = None) -> tuple[str, str, str]:
        ...