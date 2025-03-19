from setuptools import setup, find_packages

setup(
    name="bullscatch",  # Package name
    version="0.2.1",
    author="Guru Pandey",
    author_email="guru@bullscatchsecurities.com",
    description="A package for backtesting trading strategies meant for Bullscatch Securities",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/bullscatch_backtester",  # Update with your GitHub repo if available
    packages=find_packages(),
    install_requires=[
        "pandas",
        "psycopg2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,  # Ensures all necessary files inside package directories are included
)
