from setuptools import setup, find_packages

setup(
    name='sparqlin',
    version='0.1.14',
    author='Roman Korolev',
    author_email='spark_development@yahoo.com',
    description='Spark SQL framework for Databricks jobs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/rokorolev/sparqlin',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
        "pytest",
        "pyspark>=3.5.0",
        "pyyaml",
        "psutil",
        "gitpython"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    entry_points={
        "console_scripts": [
            "sparqlin=sparqlin.main:main",  # Points to the main.py script's main function
        ]
    },
)