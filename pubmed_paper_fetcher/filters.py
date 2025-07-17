from typing import List, Dict

def filter_non_academic(papers: List[Dict]) -> List[Dict]:
    return [paper for paper in papers if paper["Non-academic Author(s)"]]
