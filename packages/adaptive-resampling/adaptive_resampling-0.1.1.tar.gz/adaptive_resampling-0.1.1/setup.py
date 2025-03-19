# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="adaptive_resampling",
    version="0.1.1",
    author="Yunis Kahalan",
    author_email="ykahalan@gmail.com",
    description="A package for adaptive resampling of datasets using border detection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ykahalan/adaptive_resampling",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "scikit-learn",
    ],
)
