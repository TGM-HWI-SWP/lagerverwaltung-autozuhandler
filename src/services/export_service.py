from datetime import datetime
from pathlib import Path
import pandas as pd


class ExportService:
    def __init__(self, export_dir: str):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def export_text_report(self, filename_prefix: str, text: str) -> str:
        filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = self.export_dir / filename
        filepath.write_text(text, encoding="utf-8")
        return f"Export erfolgreich in Nextcloud:\n{filepath}"

    def export_dataframe_csv(self, df: pd.DataFrame, filename_prefix: str) -> str:
        if df.empty:
            return "Kein CSV-Export durchgeführt: Keine Daten vorhanden."
        filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = self.export_dir / filename
        df.to_csv(filepath, index=False, encoding="utf-8-sig", sep=";")
        return f"CSV exportiert:\n{filepath}"

    def export_dataframe_excel(self, df: pd.DataFrame, filename_prefix: str) -> str:
        if df.empty:
            return "Kein Excel-Export durchgeführt: Keine Daten vorhanden."
        filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = self.export_dir / filename
        df.to_excel(filepath, index=False)
        return f"Excel exportiert:\n{filepath}"