from setuptools import setup, find_packages

setup(
    name="cidre-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["netaddr==1.3.0", "requests==2.32.3"],
    entry_points={
        "console_scripts": [
            "cidre=cidre:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
