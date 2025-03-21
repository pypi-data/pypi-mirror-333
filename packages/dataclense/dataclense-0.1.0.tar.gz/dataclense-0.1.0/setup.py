from setuptools import setup, find_packages

setup(
    name="dataclense",
    version="0.1.0",
    author="Kalyanasundaram K",
    author_email="your.email@example.com",
    description="An automated data-cleaning package that handles missing values, duplicates, and formatting issues.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/palanikalyan/cleanpy",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "cleanpy=cli:main",
        ],
    },
    python_requires=">=3.6",
)
