from lxml import etree
from typing import List, Dict

def parse_papers(xml_data: str) -> List[Dict]:
    root = etree.fromstring(xml_data.encode('utf-8'))
    papers = []

    for article in root.xpath('//PubmedArticle'):
        paper = {
            "PubmedID": article.findtext('.//PMID'),
            "Title": article.findtext('.//ArticleTitle'),
            "Publication Date": article.findtext('.//PubDate/Year') or "Unknown",
            "Non-academic Author(s)": [],
            "Company Affiliation(s)": [],
            "Corresponding Author Email": "",
        }

        affiliations = article.xpath('.//AffiliationInfo')
        for aff in affiliations:
            aff_text = aff.findtext('Affiliation', default='').lower()
            name = aff.getparent().findtext('LastName', default='Unknown')

            if any(keyword in aff_text for keyword in ["pharma", "therapeutics", "biotech", "inc", "corp", "ltd", "gmbh"]):
                paper["Non-academic Author(s)"].append(name)
                paper["Company Affiliation(s)"].append(aff_text)

            if "@" in aff_text and not paper["Corresponding Author Email"]:
                email = extract_email(aff_text)
                if email:
                    paper["Corresponding Author Email"] = email

        papers.append(paper)

    return papers

def extract_email(text: str) -> str:
    import re
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else ""
