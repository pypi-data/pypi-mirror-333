from setuptools import setup, find_packages
from pathlib import Path

# Use Path object to correctly read the file
readme_path = Path(r"C:\Users\aryan\Downloads\DipoleAmplitudeModule\README.md")
long_description = readme_path.read_text()

setup(
    name='DipoleAmplitudePredictor',
    version='0.2.1',  # Increment version to reflect changes
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn==1.2.2',  # Specify the exact version
        'boto3',
        'awscli',
    ],
    description='A package for making predictions for Dipole Amplitude using a pre-trained Random Forest model',
    long_description=long_description,  # Include the README here
    long_description_content_type='text/markdown',  # Set content type as markdown
    author='Aryan Patil',
    author_email='aryanator01@gmail.com',
    url='https://github.com/aryanator/Dipole/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
