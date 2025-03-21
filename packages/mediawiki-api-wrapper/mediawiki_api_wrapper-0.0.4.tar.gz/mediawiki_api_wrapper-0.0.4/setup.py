import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mediawiki_api_wrapper",
    version="0.0.4",
    author="Mateusz Konieczny",
    description="A small wrapper around mediawiki API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeberg.org/matkoniecz/mediawiki_api_python_wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # for dependencies syntax see https://python-packaging.readthedocs.io/en/latest/dependencies.html
    install_requires = [
        'urllib3',
        'simplejson',
    ]
) 


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
