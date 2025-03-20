from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="opengeotech",
    version="0.1.0",
    author="OpenGeotech Contributors",
    author_email="opengeotechnical@gmail.com",
    description="A simple geotechnical engineering package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenGeotechnical/opengeotech-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.6",
    license="MIT",
) 