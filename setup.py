from setuptools import setup, find_packages

setup(
    name="pyrenderedterminal",
    version="0.1.2.3",
    author="Notxnorand",
    author_email="notxnor33415@gmail.com",
    description="A simple terminal graphics library for learning programming",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Notxnorand73/PyRenderedTerminal",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
    ],
    keywords="terminal graphics python education learning",
)
