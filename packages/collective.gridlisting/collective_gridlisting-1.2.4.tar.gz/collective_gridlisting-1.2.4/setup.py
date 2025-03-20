"""Installer for the collective.gridlisting package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="collective.gridlisting",
    version="1.2.4",
    description="Behavior for Folder and Collection to manipulate various appearance settings using Bootstrap (column layout) and patternslib (masonry, inject)",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS Addon folder layout masonry column grid",
    author="Peter Mathis",
    author_email="peter.mathis@kombinat.at",
    url="https://github.com/collective/collective.gridlisting",
    project_urls={
        "PyPI": "https://pypi.org/project/collective.gridlisting/",
        "Source": "https://github.com/collective/collective.gridlisting",
        "Tracker": "https://github.com/collective/collective.gridlisting/issues",
        # 'Documentation': 'https://collective.gridlisting.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "plone.api>=1.8.4",
        "plone.app.dexterity",
    ],
    extras_require={
        "test": [
            "plone.restapi",
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.contenttypes",
            "plone.app.robotframework[debug]",
        ],
    },
    entry_points="""
    [plone.autoinclude.plugin]
    target = plone
    """,
)
