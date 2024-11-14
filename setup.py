from setuptools import setup, find_packages


setup(
    name="MagisterPy",  
    version="0.1.0",  
    description="A Python package for retrieving information from magister",
    long_description=open("README.md").read(),  
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
    zip_safe=False)