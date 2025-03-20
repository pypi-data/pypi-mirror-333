from setuptools import setup, find_packages
import subprocess

# Function to install R packages
# def install_r_packages():
#     r_packages = ['readr', 'lubridate', 'dplyr', 'DatabaseConnector', 'CommonDataModel']
#     try:
#         for package in r_packages:
#             subprocess.check_call(['R', '-e', f'if (!requireNamespace("{package}", quietly = TRUE)) install.packages("{package}")'])
#     except subprocess.CalledProcessError as e:
#         print(f"Failed to install R package: {e}")

# # Install R packages before the Python package setup
# install_r_packages()

setup(
    name='cdm_csv_loader',
    version='0.1.6',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        'pandas>=1.0.0',
        'rpy2==3.5.12'
    ],
    description='A package for loading OHDSI CDM CSV files into a relational database.',
    long_description=open('README2.md').read(),  # Detailed description from your README
    long_description_content_type="text/markdown",
    author='David Chibuike Ikechi Akwuru, Jeremiah Akontomide',
    author_email='akwuru.david@ul.ie, akontomide.jeremiah@ul.ie',
    url='https://github.com/DavidIkechi/ohdsi_cdm_loader.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license="MIT",
    maintainer='David Chibuike Ikechi Akwuru, Jeremiah Akontomide',
    maintainer_email='akwuru.david@ul.ie, akontomide.jeremiah@ul.ie',
)