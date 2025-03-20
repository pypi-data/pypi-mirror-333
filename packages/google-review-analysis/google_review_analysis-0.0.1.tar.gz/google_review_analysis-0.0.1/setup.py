from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='google_review_analysis',
    version='0.0.1',
    packages=find_packages(),
    long_description = long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "tiktoken==0.9.0",
        "sentence-transformers==3.4.1",
        "transformers==4.49.0",
        "openai==1.66.3",
        "selenium==4.29.0",
        "matplotlib==3.10.1"
    ],
    author='Nikolas Kapralos',  
    description='A python library for negative google review analysis.',
    license_files = "LICENSE.txt",
    python_requires='>=3.12',

)