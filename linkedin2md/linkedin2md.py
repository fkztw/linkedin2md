from argparse import ArgumentParser

import dryscrape
import lxml.html

from bs4 import BeautifulSoup as bs


def get_args():
    parser = ArgumentParser(
        prog='linkedin2md',
        description="Export public LinkedIn resume to markdown format",
    )
    parser.add_argument(
        'linkedin_id',
        type=str,
        help="The id of the target LinkedIn profile."
    )
    args = parser.parse_args()

    return args


def get_profile_page_html(linkedin_id):
    session = dryscrape.Session(base_url="https://www.linkedin.com/in/")
    session.visit(linkedin_id)
    profile_page_html = lxml.html.tostring(session.document())

    return profile_page_html


def main():
    args = get_args()
    profile_page_html = get_profile_page_html(args.linkedin_id)
    soup = bs(profile_page_html, 'html.parser')
    print(soup.prettify())

if __name__ == "__main__":
    main()
