from setuptools import setup, find_packages

setup(
    name="CTAB_XTRA",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[],  # List dependencies here, e.g., ["numpy", "requests"]
    description="A sample Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Martin",
    author_email="martin.larsen@gmail.com",
    url="https://github.com/Kem0sabe/Package_example",  # Update with your GitHub or website
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
