from setuptools import setup, find_packages

setup(
    name="fund_insight_engine",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "financial_dataset_preprocessor>=0.2.9",
        "aws_s3_controller>=0.7.5",
    ],
    author="Juneyoung Park",
    description="A Python package providing utility functions for fund code management and analysis",
    long_description=open("README.md", encoding="utf-8").read() if open("README.md", encoding="utf-8") else "",
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
