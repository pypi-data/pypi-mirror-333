from setuptools import setup, find_packages

setup(
    name='cdm_csv_loader',
    version='0.2.0',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        'pandas>=1.0.0',
        'rpy2==3.5.12'
    ],
    description='A package for loading OHDSI CDM CSV files into a relational database.',
    long_description=open('README.md').read(),  # Detailed description from your README
    long_description_content_type="text/markdown",
    author='David Chibuike Ikechi Akwuru, Jeremiah Akintomide',
    author_email='akwuru.david@ul.ie, akintomide.jeremiah@ul.ie',
    url='https://github.com/DavidIkechi/ohdsi_cdm_loader.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license="MIT",
    maintainer='David Chibuike Ikechi Akwuru, Jeremiah Akintomide',
    maintainer_email='akwuru.david@ul.ie, akintomide.jeremiah@ul.ie',
)