from setuptools import setup, find_packages


setup(
    name="razer-dagster-manager",
    version="0.1",
    # packages=["razer_dagster_manager"],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "airbyte-cdk==0.1.53",
        "dagster==1.2.3",
        "dagster-airbyte==0.18.3",
        "dagster-managed-elements==0.18.3",
        "wheel==0.40.0",
        "pytest==7.2.2",
        "requests==2.28.2",
        "aiohttp==3.8.4",
        "asynctest==0.13.0",
    ],
)
