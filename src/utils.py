import os
from typing import Any

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def parse_excel_operations() -> list[dict[Any, Any]]:
    """Функция для считывания финансовых операций из EXCEL, выдает список словарей"""
    file_path = os.getenv("PATH_EXCEL")
    df = pd.read_excel(file_path).fillna("")
    return df.to_dict(orient="records")
