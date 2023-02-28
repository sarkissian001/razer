from setuptools import find_packages, setup

MAIN_REQUIREMENTS = [
    "airbyte-cdk~=0.1",
]



setup(
    name="source_yahoo_example",
    description="Source implementation for Yahoo Finance Price API.",
    packages=find_packages(),
    install_requires=MAIN_REQUIREMENTS
)
