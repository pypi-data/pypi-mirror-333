from setuptools import setup, find_packages

setup(
    name="conversion_unit",
    version="1.0.3",
    author="Phumin 'HourCode' Udomdach",
    author_email="phumin.udomdach@gmail.com",
    description="A powerful unit conversion library with CLI and API support",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Minkeez/conversion_unit",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
    ],
    entry_points={
        "console_scripts": [
            "convert=conversion_unit:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
