from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='korede-data-validator-tool',  # Your unique package name
    version='0.2',
    packages=find_packages(),
    install_requires=[],
    author='Oluwakorede Oyewole',
    author_email='damisonoyewole@gmail.com',
    description='A simple data validation package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-repo",  # Update this with your actual GitHub repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
