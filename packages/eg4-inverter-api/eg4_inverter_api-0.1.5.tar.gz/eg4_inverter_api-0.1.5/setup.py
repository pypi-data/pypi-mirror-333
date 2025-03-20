from setuptools import setup, find_packages

setup(
    name="eg4_inverter_api",
    version="0.1.5",
    description="A Python API for interacting with EG4 Inverter systems.",
    author="Garreth Jeremiah",
    author_email="twistedroutes76@example.com",
    url="https://github.com/twistedroutes/eg4_inverter_api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: APACHE License",
    ],
    python_requires=">=3.8",
)