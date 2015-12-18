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

    def print_summary():
        summary = get_tag_string(
            'section', class_='profile-section', id='summary'
        )
        print(summary)

    def print_experience():
        experience_tag = soup.find(
            'section', class_='profile-section', id='experience'
        )
        title = get_tag_string('h3', parent_tag=experience_tag, class_='title')
        print(title)
        print("")

        for position in experience_tag.find_all('li', class_='position'):
            title = get_tag_string(
                'h4',
                markdown=False,
                parent_tag=position,
                child_tag_name='a',
                class_='item-title'
            )
            print("+ {}".format(title))

            company = get_tag_string(
                'h5',
                markdown=False,
                parent_tag=position,
                class_='item-subtitle'
            )
            location = get_tag_string(
                'span',
                parent_tag=position,
                class_='location',
            )
            if location:
                print("{}+ {}, {}".format(markdown_indent, company, location))
            else:
                print("{}+ {}".format(markdown_indent, company))

            date_range = get_tag_string(
                'span',
                parent_tag=position,
                class_='date-range',
            )
            print("{}+ {}".format(markdown_indent, date_range))

            description = get_tag_string(
                'p',
                parent_tag=position,
                class_='description',
            )
            print("{}+ {}".format(markdown_indent, description))

    def print_education():
        education_tag = soup.find(
            'section', class_='profile-section', id='education'
        )

        title = get_tag_string('h3', parent_tag=education_tag, class_='title')
        print(title)
        print("")

        for school in education_tag.find_all('li', class_='school'):
            school_name = get_tag_string(
                'h4',
                markdown=False,
                parent_tag=school,
                class_='item-title'
            )
            date_range = get_tag_string(
                'span',
                parent_tag=school,
                class_='date-range',
            )
            print("+ {} ({})".format(school_name, date_range))

            degree = get_tag_string(
                'h5',
                markdown=False,
                parent_tag=school,
                class_='item-subtitle'
            )
            print("{}+ {}".format(markdown_indent, degree))

            description_tag = school.find('div', class_='description')
            for description in description_tag.stripped_strings:
                print("{}+ {}".format(markdown_indent, description))

    def print_skills():
        skills_tag = soup.find(
            'section', class_='profile-section', id='skills'
        )

        title = get_tag_string('h3', parent_tag=skills_tag, class_='title')
        print(title)
        print("")

        for skill in skills_tag.find_all('li', class_='skill'):
            if all(c not in ('see-more', 'see-less') for c in skill['class']):
                name = get_tag_string(None, markdown=False, parent_tag=skill)
                print("+ {}".format(name))
                # print("+ {}".format(skill.get_text().strip()))

    def print_languages():
        languages_tag = soup.find(
            'section', class_='profile-section', id='languages'
        )
        title = get_tag_string('h3', parent_tag=languages_tag, class_='title')
        print(title)
        print("")

        for language_tag in languages_tag.find_all('li', class_='language'):
            language = get_tag_string(
                'h4',
                markdown=False,
                parent_tag=language_tag,
                class_='name',
            )
            proficiency = get_tag_string(
                'p',
                markdown=False,
                parent_tag=language_tag,
                class_='proficiency',
            )
            print("+ {}: {}".format(language, proficiency))

    def print_volunteering():
        # Ignore Causes part

        volunteering_tag = soup.find(
            'section',
            class_='profile-section',
            id='volunteering'
        )
        title = get_tag_string(
            'h3',
            parent_tag=volunteering_tag,
            class_='title',
        )
        print(title)
        print("")

        for position in volunteering_tag.find_all('li', class_='position'):
            title = get_tag_string(
                'h4',
                markdown=False,
                parent_tag=position,
                class_='item-title'
            )
            organization = get_tag_string(
                'h5',
                markdown=False,
                parent_tag=position,
                class_='item-subtitle'
            )
            print("#### {} at {}".format(title, organization))

            date_range = get_tag_string(
                'span',
                parent_tag=position,
                class_='date-range',
            )
            print("{}".format(date_range))

            description = get_tag_string(
                'p',
                parent_tag=position,
                class_='description',
            )
            print("{}".format(description))
            print("")

    def print_organizations():
        organizations_tag = soup.find(
            'section',
            class_='profile-section',
            id='organizations'
        )
        title = get_tag_string(
            'h3',
            parent_tag=organizations_tag,
            class_='title',
        )
        print(title)
        print("")

        for organization_tag in organizations_tag.find_all('li'):
            organization = get_tag_string(
                'h4',
                markdown=False,
                parent_tag=organization_tag,
                class_='item-title'
            )
            position = get_tag_string(
                'h5',
                markdown=False,
                parent_tag=organization_tag,
                class_='item-subtitle'
            )
            print("#### {} at {}  ".format(position, organization))

            date_range = get_tag_string(
                'span',
                parent_tag=organization_tag,
                class_='date-range',
            )
            print("{}  ".format(date_range))

            description = get_tag_string(
                'p',
                parent_tag=organization_tag,
                class_='description',
            )
            print("{}  ".format(description))
            print("")

    def print_publications():
        publications_tag = soup.find(
            'section',
            class_='profile-section',
            id='publications'
        )
        title = get_tag_string(
            'h3',
            parent_tag=publications_tag,
            class_='title',
        )
        print(title)
        print("")

        for publication_tag in publications_tag.find_all(
            'li', class_='publication'
        ):
            publication = get_tag_string(
                'h4',
                markdown=False,
                parent_tag=publication_tag,
                class_='item-title'
            )
            url = publication_tag.find('a', class_='external-link').get('href')
            url = get_real_url(url)
            publisher = get_tag_string(
                'h5',
                markdown=False,
                parent_tag=publication_tag,
                class_='item-subtitle'
            )
            print("#### [{}]({}) on {}".format(publication, url, publisher))

            date_range = get_tag_string(
                'span',
                parent_tag=publication_tag,
                class_='date-range',
            )
            print("{}  ".format(date_range))

            description = get_tag_string(
                'p',
                parent_tag=publication_tag,
                class_='description',
            )
            print("{}  ".format(description))
            print("")

    def print_awards():
        awards_tag = soup.find(
            'section',
            class_='profile-section',
            id='awards'
        )
        title = get_tag_string(
            'h3',
            parent_tag=awards_tag,
            class_='title',
        )
        print(title)
        print("")

        for award_tag in awards_tag.find_all('li', class_='award'):
            award = get_tag_string(
                'h4',
                markdown=False,
                parent_tag=award_tag,
                class_='item-title'
            )
            print("#### {}".format(award))

            issuer = get_tag_string(
                'h5',
                markdown=False,
                parent_tag=award_tag,
                class_='item-subtitle'
            )
            date_range = get_tag_string(
                'span',
                parent_tag=award_tag,
                class_='date-range',
            )
            print("Held by {} at {}  ".format(issuer, date_range))

            description = get_tag_string(
                'p',
                parent_tag=award_tag,
                class_='description',
            )
            print("{}  ".format(description))
            print("")

    def print_projects():
        projects_tag = soup.find(
            'section',
            class_='profile-section',
            id='projects'
        )
        title = get_tag_string(
            'h3',
            parent_tag=projects_tag,
            class_='title',
        )
        print(title)
        print("")

        for project_tag in projects_tag.find_all('li', class_='project'):
            project = get_tag_string(
                'h4',
                markdown=False,
                parent_tag=project_tag,
                class_='item-title'
            )
            url = project_tag.find('a', class_='external-link').get('href')
            url = get_real_url(url)
            print("#### [{}]({})".format(project, url))

            date_range = get_tag_string(
                'span',
                parent_tag=project_tag,
                class_='date-range',
            )
            print("{}  ".format(date_range))

            description = get_tag_string(
                'p',
                parent_tag=project_tag,
                class_='description',
            )
            print("{}  ".format(description))
            print("")

    print_headline()
    print_markdown_hr()
    print_summary()
    print_markdown_hr()
    print_experience()
    print_markdown_hr()
    print_education()
    print_markdown_hr()
    print_skills()
    print_markdown_hr()
    print_languages()
    print_markdown_hr()
    print_volunteering()
    print_markdown_hr()
    print_organizations()
    print_markdown_hr()
    print_publications()
    print_markdown_hr()
    print_awards()
    print_markdown_hr()
    print_projects()
    print_markdown_hr()


def main():
    args = get_args()
    profile_page_html = get_profile_page_html(args.linkedin_id)
    print_profile_in_markdown(profile_page_html)

if __name__ == "__main__":
    main()
