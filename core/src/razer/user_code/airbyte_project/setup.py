from setuptools import find_packages, setup

setup(
    name="airbyte_project",
    packages=find_packages(exclude=["airbyte_project_tests"]),
    install_requires=[
        "dagster",
        "dagster-airbyte",
        "dagster-managed-elements",
        "dagster-dbt",
        "dagster-postgres",
        "pandas",
        "dbt-core",
        "dbt-postgres",
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
