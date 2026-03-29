from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="pyrenderedterminal",
    version="0.1.2.5",
    author="Notxnorand",
    author_email="notxnor33415@gmail.com",
    description="A simple terminal graphics library for learning programming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Notxnorand73/PyRenderedTerminal",
    project_urls={
        "Documentation": "https://github.com/Notxnorand73/PyRenderedTerminal/blob/main/docs.html",
        "Source": "https://github.com/Notxnorand73/PyRenderedTerminal",
    },
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries",
        "Topic :: Games/Entertainment",
    ],
    keywords="terminal graphics python education learning",
)
