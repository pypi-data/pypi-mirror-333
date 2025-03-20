"""Installer for the design.plone.opendata package."""

from pathlib import Path
from setuptools import find_packages
from setuptools import setup


long_description = f"""
{Path("README.md").read_text()}\n
{Path("CONTRIBUTORS.md").read_text()}\n
{Path("CHANGES.md").read_text()}\n
"""


setup(
    name="design.plone.opendata",
    version="1.0.0a0",
    description="Plone DCAT IT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="RedTurtle",
    author_email="info@redturtle.it",
    url="https://github.com/RedTurtle/design.plone.opendata",
    project_urls={
        "PyPI": "https://pypi.org/project/design.plone.opendata",
        "Source": "https://github.com/RedTurtle/design.plone.opendata",
        "Tracker": "https://github.com/RedTurtle/design.plone.opendata/issues",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["design", "design.plone"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "setuptools",
        "Plone",
        "plone.api",
        "plone.restapi",
        # "design.plone.contenttypes",
        "rdflib",
    ],
    extras_require={
        "test": [
            "zest.releaser[recommended]",
            "zestreleaser.towncrier",
            "plone.app.testing",
            "plone.restapi[test]",
            "pytest",
            "pytest-cov",
            "pytest-plone>=0.5.0",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    """,
)
