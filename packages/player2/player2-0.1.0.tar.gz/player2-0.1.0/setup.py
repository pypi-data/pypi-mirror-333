from setuptools import setup, find_packages

setup(
    name="player2",
    version="0.1.0",
    packages=find_packages(),
    author="EAMCVD",
    author_email="info@axiom-mc.org",
    description="A namespace package for player2",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://player2.game",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
