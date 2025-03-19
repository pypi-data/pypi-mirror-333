from setuptools import setup, find_packages

setup(
    name="py-r-fst",
    version="0.1.1",
    packages=find_packages(),
    package_data={"": ["*.py"]},
    py_modules=["pyfst"],
    install_requires=[
        "pandas>=1.0.0",
        "rpy2>=3.4.0",
    ],
    author="msdavid",
    author_email="mauro@sauco.net",
    description="Python wrapper for the R fst package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/msdavid/py-r-fst",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)