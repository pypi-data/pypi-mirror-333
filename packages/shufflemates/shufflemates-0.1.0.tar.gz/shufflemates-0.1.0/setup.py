from setuptools import setup, find_packages

setup(
    name="shufflemates",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Ian Park",
    author_email="ianolpx@gmail.com",
    description="A Python package for randomly grouping students or teams.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ianolpx/shufflemates",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
