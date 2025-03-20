from setuptools import setup, find_packages

setup(
    name="latex_generator_neimess_itmo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Maxim Gavrilenko",
    author_email="sh0ckerZ7714@gmail.com",
    description="A simple package to generate LaTeX tables and images",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
