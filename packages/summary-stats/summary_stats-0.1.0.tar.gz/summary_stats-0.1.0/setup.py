from setuptools import setup, find_packages

setup(
    name="summary_stats",
    version="0.1.0",
    description="A simple Python package for generating summary statistics of pandas DataFrames",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=["pandas"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
