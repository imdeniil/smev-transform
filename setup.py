"""
Setup script for smev-transform Python package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smev-transform",
    version="2.0.0",
    author="Daniil",
    author_email="keemor821@gmail.com",
    description="Реализация алгоритма трансформации urn://smev-gov-ru/xmldsig/transform для СМЭВ 3.5.0.27",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imdeniil/smev-transform",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="smev смэв xml xmldsig transformation gosuslugi",
    project_urls={
        "Bug Reports": "https://github.com/imdeniil/smev-transform/issues",
        "Source": "https://github.com/imdeniil/smev-transform",
        "Documentation": "https://info.gosuslugi.ru/docs/section/%D0%A1%D0%9C%D0%AD%D0%92/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5_%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B/%D0%A1%D0%9C%D0%AD%D0%923/?id=758",
    },
)