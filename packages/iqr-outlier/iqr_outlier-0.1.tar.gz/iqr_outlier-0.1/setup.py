from setuptools import setup, find_packages

setup(
    name="iqr_outlier",
    version="0.1",
    packages=find_packages(),
    install_requires=["numpy", "pandas"],
    description="A simple library to detect and remove outliers using IQR.",
    author="Abhinav Masih",
    author_email="abhnv.msh@gmail.com",
    url="https://github.com/abhi-2301-git/iqr_outlier",
)
