# O setup.py é o script que permite instalar a biblioteca via pip.

from setuptools import setup, find_packages

setup(
    name="logging_emr",
    version="0.1.4",
    author="Agibank Data Engineering",
    description="Biblioteca para logging de processos do EMR no AWS CloudWatch",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "boto3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

# Linhas removidas do setup()
    #author_email="",
    #url="https://github.com/lalala/logging_emr",