# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import io

# Lee README.md con codificación UTF-8 explícita
with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fin-stresstest",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "statsmodels>=0.12.0",
        "yfinance>=0.2.0",
    ],
    author="Luis Humberto Calderon Baldeón",
    author_email="luis.calderon.b@uni.pe",
    description="Herramienta para análisis de escenarios de estrés financiero",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LuisHCalderon/StressTest",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.7",
)