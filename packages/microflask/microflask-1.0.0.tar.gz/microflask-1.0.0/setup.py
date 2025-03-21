from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="microflask",
    version="1.0.0",
    author="Michael Hudelson",
    author_email="michaelhudelson@gmail.com",
    description="This project contains bootstrap code to speed up the development of AWS based microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=[
        "microflask",
        "microflask.constants",
        "microflask.security"
    ],
    install_requires=[
        "boto3",
        "flask",
        "flask-classful",
        "redis",
        "requests"
    ],
    python_requires=">=3.7",
)
