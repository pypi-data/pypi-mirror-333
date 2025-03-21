from setuptools import setup, find_packages

setup(
    name="Snowforge-package",
    version="0.1.0",  # Change this for new releases
    author="Andreas Heggelund",
    author_email="andreasheggelund@gmail.com",
    description="A Python package for integrations to Snowflake and AWS as well as many support scripts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Snowforge",  # Replace with your GitHub repo
    packages=find_packages(),
    install_requires=[
        "boto3",
        "snowflake-connector-python",
        "coloredlogs",
        "colored",
        "tqdm",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
