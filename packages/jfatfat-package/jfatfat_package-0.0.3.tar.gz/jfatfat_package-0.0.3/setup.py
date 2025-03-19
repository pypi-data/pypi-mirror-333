from setuptools import setup, find_packages


setup(
    name="jfatfat_package",
    version="0.0.3",
    author="Jihad Fatfat",
    author_email="jihadmohfatfat1999@gmail.com",
    description="A simple utility package",
    long_description=open("README.txt").read(),
    long_description_content_type="text/plain",
    url="https://github.com/jihadfatfat99/Python-Piscine/00/ex09/ft-package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
