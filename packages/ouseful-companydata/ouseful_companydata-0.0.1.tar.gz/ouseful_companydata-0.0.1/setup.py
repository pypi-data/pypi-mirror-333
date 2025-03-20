from setuptools import setup, find_packages

setup(
    name="ouseful_companydata",
    version="0.0.1",
    packages=["ouseful_companydata"],  # "otherpackage": "../../somewhere_else/src",
    install_requires=[
        "networkx",
        "pandas",
        "requests",
        "requests-cache",
    ],
    author="Tony Hirst",
    author_email="tony.hirst@gmail.com",
    description="ouseful datasupply package for working with Companies House data and creating co-director graphs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ouseful-datasupply/companydata",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
