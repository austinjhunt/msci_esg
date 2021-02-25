import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-msci-esg", # Replace with your own username
    version="0.0.3",
    author="Austin Hunt",
    author_email="huntaj@g.cofc.edu",
    description="A package for scraping content from the MSCI.com ESG Ratings Corporate Search Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/austinjhunt/msci_esg",
    project_urls={
        "Bug Tracker": "https://github.com/austinjhunt/msci_esg/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "requests","selenium"
    ]
)