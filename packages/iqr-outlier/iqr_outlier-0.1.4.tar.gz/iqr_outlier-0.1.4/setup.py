from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read() 

setup(
    name="iqr_outlier",
    version="0.1.4",
    packages=find_packages(),
    install_requires=["pandas", "numpy"],
    description="A library to detect and remove outliers using IQR.",
    long_description=long_description,
    long_description_content_type="text/markdown",  
    author="Abhinav Masih",
    author_email="abhnv.msh@gmail.com",
    url="https://github.com/abhi-2301-git/iqr_outlier",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
