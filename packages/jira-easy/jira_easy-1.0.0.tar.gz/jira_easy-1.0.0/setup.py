from setuptools import setup, find_packages

setup(
    name="jira_easy",
    version="1.0.0",
    description="A simple Python library for fetching and creating JIRA issues using JQL.",
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