#!/usr/bin/env python3
"""
Setup script for Fawaz: Proxy Tester (Fwz_PT)
A multi-threaded proxy testing tool for HTTP/SOCKS5 proxies
"""

import os
import sys
from setuptools import setup, find_packages

# Ensure we're using Python 3.7+
if sys.version_info < (3, 7):
    sys.exit("Python 3.7 or higher is required for Fwz_PT")

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "A multi-threaded proxy testing tool for HTTP/SOCKS proxies"

# Read requirements from requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return [
        'httpx[socks]>=0.25.0',
        'rich>=13.0.0',
        'requests>=2.28.0',
        'pysocks>=1.7.1',
        'pyfiglet>=0.8.0',
        'colorama>=0.4.6'
    ]

# Get version from src/__init__.py or use default
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'src', '__init__.py')
    if os.path.exists(version_file):
        with open(version_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"\'')
    return "1.0.0"

setup(
    name="fwz_pt",
    version=get_version(),
    author="Fawaz Al-Ghzawi",
    author_email="Ghazawe1@gmail.com",
    description="A multi-threaded proxy testing tool for HTTP/SOCKS5 proxies",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/fawaz7/Proxy-tester",
    project_urls={
        "Bug Reports": "https://github.com/fawaz7/Proxy-tester/issues",
        "Source": "https://github.com/fawaz7/Proxy-tester",
        "Documentation": "https://github.com/fawaz7/Proxy-tester/wiki",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ],
    keywords="proxy, testing, http, socks, socks5, network, tool, multi-threaded",
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "build": [
            "build>=0.8.0",
            "twine>=4.0.0",
            "wheel>=0.37.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fwz_pt=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["*.py"],
        "data": ["*.txt"],
        "docs": ["*.md"],
    },
    zip_safe=False,  # Allow access to package data files
    platforms=["Windows", "Linux", "macOS", "Unix"],
    license="MIT",
    license_files=["LICENSE"],
)
