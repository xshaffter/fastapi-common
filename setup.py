from setuptools import find_packages, setup
from common.fastapi import __version__
requirements = [
    "fastapi",
    "requests",
    "SQLAlchemy",
    "uvicorn",
    "pytest",
    "pydantic",
    "boto3",
]

setup(
    name="fastapi-common",
    version=__version__,
    url="https://github.com/xshaffter/fastapi-common",
    description="Custom Fastapi library and tools",
    readme="README.md",
    author="Alfredo Martinez",
    author_email="xshaffter@gmail.com",
    maintainer="Alfredo Martínez",
    maintainer_email="xshaffter@gmail.com",
    packages=find_packages(exclude=("tests",)),
    namespace_packages=["common"],
    install_requires=requirements,
    license="GNU GPL 3.0",
    python_requires=">=3.8.0",
)
