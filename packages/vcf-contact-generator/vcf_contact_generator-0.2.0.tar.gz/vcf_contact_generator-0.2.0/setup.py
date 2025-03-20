from setuptools import setup, find_packages

setup(
    name="vcf-contact-generator",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[], 
    author="Szymon Małachowski",
    author_email="szymonmalachowski.1@gmail.com",
    description="A simple package to create vCard (.vcf) files",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/qmpel22/vcf_contact_generator",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
