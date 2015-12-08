#!/usr/bin/env python3

from setuptools import find_packages, setup

import linkedin2md


setup(
    packages=find_packages(exclude=["linkedin2md.bin"]),
    scripts=["linkedin2md/bin/linkedin2md"],
    install_requires=['dryscrape', 'beautifulsoup4'],
    name="linkedin2md",
    version=linkedin2md.__version__,
    author="Shun-Yi Jheng",
    author_email="M157q.tw@gmail.com",
    url="https://github.com/M157q/linkedin2md",
    keywords="LinkedIn, markdown, resume",
    description="Export public LinkedIn resume to markdown format",
    platforms=['Linux'],
    license='GPLv3',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
)
