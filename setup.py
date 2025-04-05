from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


setup(
    name="MagisterPy",
    version="0.1.41",
    description="A Python package for retrieving information from magister",
    long_description=open("./README.MD").read(),
    long_description_content_type="text/markdown",
    author="H3LL0U",
    url="https://github.com/H3LL0U/MagisterPy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    include_package_data=True,
    zip_safe=False,
    install_requires=parse_requirements(
        './requirements.txt')  # Read dependencies
)
