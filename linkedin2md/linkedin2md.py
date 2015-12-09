from argparse import ArgumentParser
from collections import OrderedDict

import dryscrape
import lxml.html

from bs4 import BeautifulSoup as bs
from html2text import html2text


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


def print_profile_in_markdown(profile_page_html):
    soup = bs(profile_page_html, 'html.parser')

    def print_markdown_hr():
        print("")
        print("---")
        print("")

    def get_tag_string(name, **attrs):
        tag = soup.find(name, **attrs)

        try:
            string = tag.string.strip()
        except AttributeError:
            return ''
        else:
            return string

    def get_table_dict(**attrs):
        table = soup.find('table', **attrs)

        try:
            rows = table.find_all('tr')
        except AttributeError:
            return {}
        else:
            table_dict = OrderedDict()

            for row in rows:
                th, td = map(str.strip, html2text(row.prettify()).split('|'))
                table_dict[th] = td

            return table_dict

    def print_headline():
        name = get_tag_string('h1', class_='fn', id='name')
        extra_info = get_table_dict(class_='extra-info')

        print("## {}".format(name))
        print("")
        for th, td in extra_info.items():
            print("+ {}".format(th))
            for d in map(str.strip, td.split('\n')):
                if d.endswith(','):
                    d = d[:-1]
                print("    {}".format(d))

    print_headline()
    print_markdown_hr()


def main():
    args = get_args()
    profile_page_html = get_profile_page_html(args.linkedin_id)
    print_profile_in_markdown(profile_page_html)

    # with open('./tests/profile.html') as profile_page_html:
        # print_profile_in_markdown(profile_page_html)

if __name__ == "__main__":
    main()
