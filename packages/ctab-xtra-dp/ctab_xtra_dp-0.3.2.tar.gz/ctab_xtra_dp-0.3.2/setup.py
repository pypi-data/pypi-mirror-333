from setuptools import setup, find_packages
import os
folder = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(folder, "ctab_xtra_dp", "README.md")


try:
    with open(readme_path) as f:
        long_description = f.read()
except FileNotFoundError:
    print(f"README not found at {readme_path}!")
    long_description = "Description not available"


setup(
    name="ctab_xtra_dp",
    version="0.3.2",
    packages=find_packages(),
    install_requires=[],  # List dependencies here, e.g., ["numpy", "requests"]
    description="A sample Python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="kem0sabe",
    author_email="martivl@stud.ntnu.no",
    url="https://github.com/Kem0sabe/Package_example",  # Update with your GitHub or website
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
