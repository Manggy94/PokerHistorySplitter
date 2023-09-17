from pathlib import Path
from setuptools import setup, find_packages

install_requires = [
    "boto3",
    "pythondotenv"
    ]

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Natural Language :: French",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Games/Entertainment",
    "Topic :: Games/Entertainment :: Board Games"
]

setup(
    name="pkrhistorysplitter",
    version="0.0.1",
    description="A Poker Package to split poker history files in DO S3 bucket",
    long_description=Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    classifiers=classifiers,
    keywords="poker pkrhistory history pkr pkrhistorysplitter pokerhistory splitter downloader",
    author="Alexandre MANGWA",
    author_email="alex.mangwa@gmail.com",
    url="https://github.com/manggy94/PokerHistorySplitter",
    license_file='LICENSE.txt',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=["pytest", "pytest-cov", "coverage", "coveralls"],
)