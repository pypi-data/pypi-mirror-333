from setuptools import setup, find_packages
setup(
name='flask_pdf_extractor',
version='1.0.0',
author='bhavesh_kumar',
author_email='kumarbhavesh8298@gmail.com',
description='pdf extraction package',
packages=find_packages(),
include_package_data=True,
install_requires=[
    "Flask",
    "PyPDF2",
    "ollama",
    "python-dotenv"
],
entry_points={
    "console_scripts": [
        "pdf-extractor=flask_pdf_extractor.app:main"
    ]
},
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.10',
)

