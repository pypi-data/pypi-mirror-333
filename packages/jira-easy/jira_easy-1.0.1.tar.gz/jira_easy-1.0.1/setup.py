import pathlib
from setuptools import setup, find_packages

# Read the contents of README.md
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="jira_easy",
    version="1.0.1",
    description="A simple Python library for fetching JIRA issues using JQL.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Abdulhamit Güngören",
    author_email="abdulhamitgungoren@gmail.com",
    url="https://github.com/ahgq7/jira_easy",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
