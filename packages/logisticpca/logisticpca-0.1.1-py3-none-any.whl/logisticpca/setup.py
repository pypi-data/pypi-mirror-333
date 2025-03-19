from setuptools import setup, find_packages

setup(
    name="logisticpca",  # Package name users will install via pip
    version="0.1.0",  # Update version numbers for new releases
    packages=find_packages(),
    install_requires=[
        "torch",
        "numpy"
    ],
    author="Reda Abouzaid",
    author_email="azaidr00@gmail.com",
    description="A Python implementation of Logistic PCA for binary data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/azaidr/logisticpca",  # Your GitHub repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
