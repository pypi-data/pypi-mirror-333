# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

setup(
    name="fin-stresstest",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "statsmodels>=0.12.0",
    ],
    author="Luis Humberto Calderon Baldeón",
    author_email="luis.calderon.b@uni.pe",
    description="Herramienta para análisis de escenarios de estrés financiero",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/StressTest",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.7",
)