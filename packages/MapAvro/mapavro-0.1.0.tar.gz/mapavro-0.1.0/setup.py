from setuptools import setup, find_packages

setup(
    name="MapAvro",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "setuptools",
        "bnunicodenormalizer"
    ],
    author="Shahriar Kabir Nahin",
    # author_email="",
    description="A package for converting Bengali text to Avro and vice versa.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SKNahin/MapAvro",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    license="MIT"
)