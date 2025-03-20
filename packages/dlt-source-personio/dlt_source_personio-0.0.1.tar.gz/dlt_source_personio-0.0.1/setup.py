from setuptools import setup, find_packages

setup(
    name="dlt-source-personio",
    version="0.0.1",
    author="Planet A GmbH",
    author_email="dev@planet-a.com",
    packages=find_packages(exclude=["tests"]),
    description="A DLT source for personio",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "dlt>=1.8.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
