from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="aleph-superfluid",
    version="0.2.2",
    description="Fork of the Python SDK for the Superfluid Protocol",
    package_dir={"": "main"},
    packages=find_packages(where="main"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aleph-im/superfluid.py",
    author="Godspower-Eze",
    author_email="Godspowereze260@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    install_requires=["web3 == 6.3.0", "python-decouple==3.8"],
    extras_require={
        "dev": ["twine>=4.0.2"]
    },
    python_requires=">=3"
)
