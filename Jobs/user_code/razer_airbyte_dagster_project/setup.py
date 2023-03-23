from setuptools import find_packages, setup
import os

setup(
    name="airbyte_project",
    packages=find_packages(exclude=["airbyte_project_tests"]),
    install_requires=[
        "dagster",
        "dagster-airbyte",
        "dagster-managed-elements",
        'razer-dagster-manager @ file://' + os.path.abspath('razer_dagster_manager-0.1-py3-none-any.whl'),
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
