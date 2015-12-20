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

    del session
    return profile_page_html


def get_real_url(url):
    session = dryscrape.Session()
    session.visit(url)
    real_url = session.url()

    del session
    return real_url


def print_profile_in_markdown(profile_page_html):
    soup = bs(profile_page_html, 'html.parser')
    markdown_indent = ' '*4

    def print_markdown_hr():
        print("")
        print("---")
        print("")

    def get_tag_string(
        name, markdown=True, parent_tag=None, child_tag_name=None, **attrs
    ):

        if parent_tag is None:
            tag = soup.find(name, **attrs)
        else:
            tag = parent_tag.find(name, **attrs)

        if child_tag_name:
            tag = tag.find(child_tag_name)

        try:
            if markdown:
                string = html2text(tag.prettify()).strip()
            else:
                string = tag.get_text().strip()
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
        print(name)
        print("")

        extra_info = get_table_dict(class_='extra-info')
        for th, td in extra_info.items():
            print("+ {}".format(th))
            for d in map(str.strip, td.split('\n')):
                if d.endswith(','):
                    d = d[:-1]
                print("{}{}".format(markdown_indent, d))

    def print_section(tag, sub_tag_class):
        title = get_tag_string(
            'h3',
            parent_tag=tag,
            class_='title',
        )
        print(title)
        print("")

        item_tags = tag.find_all('li', class_=sub_tag_class)

        if item_tags:
            for item_tag in item_tags:
                item_title = get_tag_string(
                    'h4',
                    markdown=False,
                    parent_tag=item_tag,
                )
                url = item_tag.find('a', class_='external-link')
                if url:
                    url = url.get('href')
                    url = get_real_url(url)

                if item_title and url:
                    print("#### [{}]({})".format(item_title, url))
                elif item_title:
                    print("#### {}".format(item_title))

                item_subtitle = get_tag_string(
                    'h5',
                    markdown=False,
                    parent_tag=item_tag,
                    class_='item-subtitle'
                )
                if item_subtitle:
                    print("+ {}".format(item_subtitle))

                date_range = get_tag_string(
                    'span',
                    parent_tag=item_tag,
                    class_='date-range',
                )
                if date_range:
                    print("+ {}".format(date_range))

                description = get_tag_string(
                    'p',
                    parent_tag=item_tag,
                )
                if description:
                    print("")
                    print("{}  ".format(description.replace('\n', '  \n')))

                skill = get_tag_string(
                    'span',
                    parent_tag=item_tag,
                    class_='wrap',
                )
                if skill:
                    print("+ {}".format(skill))

                if item_title:
                    print("")

        else:
            description = get_tag_string(
                'p',
                parent_tag=tag,
            )
            if description:
                print("")
                print("{}  ".format(description.replace('\n', '  \n')))

    print_headline()
    print_markdown_hr()
    sections = (
        # ('topcard', ''),
        ('summary', ''),
        ('experience', 'position'),
        ('education', 'school'),
        ('skills', 'skill'),
        ('languages', 'language'),
        ('volunteering', 'position'),
        ('organizations', ''),
        ('publications', 'publication'),
        ('awards', 'award'),
        ('projects', 'project'),
        ('scores', 'score'),
    )
    for section, section_sub_tag_class in sections:
        tag = soup.find(
            'section',
            class_='profile-section',
            id=section,
        )
        print_section(tag, section_sub_tag_class)
        print_markdown_hr()


def main():
    args = get_args()
    profile_page_html = get_profile_page_html(args.linkedin_id)
    print_profile_in_markdown(profile_page_html)

if __name__ == "__main__":
    main()
