from setuptools import find_packages, setup

setup(
    name="mytoolsID",
    version="0.6.dev1",
    description="Library of @NorSodikin",
    long_description="A collection of useful tools and utilities.",
    long_description_content_type="text/markdown",
    author="NorSodikin",
    author_email="admin@NorSodikin.com",
    url="https://github.com/SenpaiSeeker/tools",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8, <3.13",
    install_requires=["cryptography", "pyrogram-dev", "tgcrypto", "gpytranslate", "google-generativeai"],
)
