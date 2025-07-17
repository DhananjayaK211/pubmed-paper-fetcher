import pandas as pd
from typing import List, Dict

def export_to_csv(papers: List[Dict], filename: str) -> None:
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
