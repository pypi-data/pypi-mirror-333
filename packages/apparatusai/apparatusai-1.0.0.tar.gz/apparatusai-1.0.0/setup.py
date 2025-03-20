from setuptools import setup, find_packages

setup(
    name="apparatusai",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    author="Basab Jha",
    author_email="basab@apparatusai.space",
    description="Python SDK for ApparatusAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/comethrusws/apparatusai-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

