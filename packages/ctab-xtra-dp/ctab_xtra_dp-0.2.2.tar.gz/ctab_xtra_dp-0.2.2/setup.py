from setuptools import setup, find_packages

setup(
    name="ctab_xtra_dp",
    version="0.2.2",
    packages=find_packages(),
    install_requires=[],  # List dependencies here, e.g., ["numpy", "requests"]
    description="A sample Python package",
    long_description=open("README.md").read(),
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
