# setup.py

from setuptools import setup, find_packages

setup(
    name="mouse_analysis",
    version="0.1.0",
    author="Fengxi Jin",
    author_email="fengxi.jin@manchester.ac.uk",
    description="A package for analyzing mouse behavior.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mouse_analysis",  # Update with your repo URL if available
    packages=find_packages(),
    install_requires=[
        "numpy>=1.15",  # Adjust as necessary
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Change license if needed
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
