from setuptools import setup, find_packages
import re

def get_version():
    with open("mockpy/__init__.py", "r", encoding="utf-8") as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python-mockpy",
    version=get_version(),
    author="Reloading",
    author_email="reloading001@hotmail.com",
    description="Comprehensive realistic data generation library for testing and development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/burakozcn01/mockpy",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'mockpy.data.locales': ['*.json'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "full": ["translators", "jsonschema", "django", "flask", "sqlalchemy", "pydantic", "numpy"],
        "translate": ["translators"],
        "jsonschema": ["jsonschema"],
        "django": ["django"],
        "flask": ["flask"],
        "sqlalchemy": ["sqlalchemy"],
        "fastapi": ["fastapi", "pydantic"],
        "dev": ["pytest", "pytest-cov", "black", "isort", "flake8", "pylint"],
        "performance": ["numpy"], 
    },
    keywords=["mock", "fake", "data", "testing", "development", "faker", "generator", 
             "test data", "random data", "dummy data", "sample data"],
    project_urls={
        "Bug Reports": "https://github.com/burakozcn01/mockpy/issues",
        "Source": "https://github.com/burakozcn01/mockpy",
    },
)