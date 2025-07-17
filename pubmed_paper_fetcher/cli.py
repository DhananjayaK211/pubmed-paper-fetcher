import argparse
from pubmed_paper_fetcher import api, parser, filters, utils

def main():
    parser_cli = argparse.ArgumentParser(description="Fetch PubMed papers with biotech affiliations.")
    parser_cli.add_argument("query", type=str, help="PubMed search query")
    parser_cli.add_argument("--debug", "-d", action="store_true", help="Enable debug mode")
    parser_cli.add_argument("--file", "-f", type=str, help="Output CSV filename")

    args = parser_cli.parse_args()

    if args.debug:
        print(f"[DEBUG] Query: {args.query}")

    try:
        ids = api.fetch_pubmed_ids(args.query)
        if args.debug:
            print(f"[DEBUG] Fetched PubMed IDs: {ids}")

        xml_data = api.fetch_paper_details(ids)
        papers = parser.parse_papers(xml_data)

        filtered = filters.filter_non_academic(papers)
        if args.debug:
            print(f"[DEBUG] Filtered Papers: {len(filtered)} / {len(papers)}")

        if args.file:
            utils.export_to_csv(filtered, args.file)
            print(f"[✓] Results saved to {args.file}")
        else:
            for paper in filtered:
                print(paper)

    except Exception as e:
        print(f"[ERROR] {e}")
