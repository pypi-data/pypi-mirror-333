from setuptools import find_packages, setup
import os

# Optional: read the long description from README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="bayesNestor",
    version="0.1.5",
    description=(
        "Nestor is a Bayesian Network implementation designed to dynamically "
        "generate personalized learning paths tailored to the unique psychological "
        "traits of each learner, optimizing educational outcomes."
    ),
    author="Robert Maier & Vamsi Krishna Nadimpalli",
    author_email="robert.maier@othr.de & vamsi.nadimpalli@oth-regensburg.de",
    license="MIT",
    packages=find_packages(),
    package_data={
        "pynestor.data": ["*.xml"],
        "pynestor.core.io.validation_files": ["*.xsd", "*.dtd"],
    },
    install_requires=[
        "dowhy==0.11.1",
        "lxml>=5.2",
        "matplotlib>=3.9",
        "networkx>=3.2",
        "numpy==1.26.4",
        "pandas>=2.2",
        "pgmpy>=0.1.24",
        "pyAgrum==1.15.0",
        # "pygraphviz==1.13"
        "pytest>=8.2",
        "setuptools>=71.1",
        "Sphinx>=7.4",
        "torch==2.3.1",  # see fbgemm.dll error (https://github.com/pytorch/pytorch/issues/131662)
        "ipython>=8.16",
        "tabulate>=0.9.0",
        "dash>=2.16.0",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
)
