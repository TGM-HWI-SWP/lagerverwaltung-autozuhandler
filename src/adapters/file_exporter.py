from __future__ import annotations
 
from datetime import datetime
from pathlib import Path
 
import pandas as pd
 
from src.ports.export_ports import ExportPort
 
 
class FileExporter(ExportPort):
    def __init__(self, export_dir: Path) -> None:
        self._export_dir = export_dir
        self._export_dir.mkdir(parents=True, exist_ok=True)
 
    def export_text(self, filename_prefix: str, text: str) -> str:
        filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = self._export_dir / filename
        filepath.write_text(text, encoding="utf-8")
        return f"Export erfolgreich:\n{filepath}"
 
    def export_csv(self, df: pd.DataFrame, filename_prefix: str) -> str:
        if df.empty:
            return "Kein CSV-Export durchgeführt: Keine Daten vorhanden."
        filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = self._export_dir / filename
        df.to_csv(filepath, index=False, encoding="utf-8-sig", sep=";")
        return f"CSV exportiert:\n{filepath}"
 
    def export_excel(self, df: pd.DataFrame, filename_prefix: str) -> str:
        if df.empty:
            return "Kein Excel-Export durchgeführt: Keine Daten vorhanden."
        filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = self._export_dir / filename
        df.to_excel(filepath, index=False)
        return f"Excel exportiert:\n{filepath}"