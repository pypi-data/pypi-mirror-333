from setuptools import setup, find_packages

setup(
    name="ssl-analyzer",
    version="0.1.1",
    author="Tirumala Krishna Mohan Gudimalla",
    author_email="krishnamohan.t93@gmail.com",
    description="A Python package to analyze SSL certificates",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TirumalaKrishnaMohanG",
    packages=find_packages(),
    install_requires=[
        "cryptography",
    ],
    entry_points={
        "console_scripts": [
            "ssl-analyzer=ssl_analyzer.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
