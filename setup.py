from setuptools import find_packages, setup


setup(
    name="py-vertica-prom",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "vertica-python",
        "prometheus-client"
    ],
)
