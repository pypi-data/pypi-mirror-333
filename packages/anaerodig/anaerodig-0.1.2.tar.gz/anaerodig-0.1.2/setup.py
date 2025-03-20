from setuptools import find_packages, setup

long_description = "".join(
    [
        "Anaerobic Digestion models in Python\n",
        "This package structures AD models around configuration,",
        "feed, and initial state objects.\n",
        "Implementations of ADM1 and AM2 models are available in submodules",
        "'pyadm1' and 'pyam2'",
    ]
)

setup(
    name="anaerodig",
    version="0.1.2",
    author="Antoine Picard-Weibel",
    author_email="apicard.w@gmail.com",
    description="Anaerobic Digestion models, in python",
    long_description=long_description,
    packages=find_packages(),
    package_data={"anaerodig": ["*/data/*.json", "*/data/*.csv"]},
    install_requires=[
        "apicutils>=0.0.3",
        "pandas",
        "scipy>=1.7.0",
        "numpy<=1.26",
        "numba==0.58.1",
        "multiprocess>=0.70",
        "matplotlib>=3.7.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
