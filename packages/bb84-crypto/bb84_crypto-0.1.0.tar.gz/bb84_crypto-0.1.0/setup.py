from setuptools import setup, find_packages

setup(
    name="bb84_crypto",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    author="Amir",
    author_email="ak2testspace@gmail.com",
    description="A simple implementation of the BB84 quantum key distribution protocol.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bb84_crypto",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
