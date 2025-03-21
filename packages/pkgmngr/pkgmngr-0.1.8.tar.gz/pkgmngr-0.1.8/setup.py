from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pkgmngr",
    version="0.1.8",
    author="Baptiste FERRAND",
    author_email="bferrand.maths@gmail.com",
    description="Comprehensive Python package utilities for creation, snapshotting, and lifecycle management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/B4PT0R/pkgmngr",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",     # For GitHub API interactions
        "toml>=0.10.2",         # For config file parsing
        "pathspec>=0.9.0",      # For gitignore pattern matching
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.12.0',
            'flake8>=3.9.0',
            'black>=21.5b2',
            'coverage>=5.5',
            'build>=0.7.0',
            'twine>=3.4.1',
            'isort>=5.9.1',
        ],
    },
    entry_points={
        'console_scripts': [
            'pkgmngr=pkgmngr.__main__:main',
        ],
    },
    keywords="package, utilities, snapshot, backup, restore, versioning, creation, github, lifecycle, documentation, python-package",
    project_urls={
        "Bug Reports": "https://github.com/B4PT0R/pkgmngr/issues",
        "Source": "https://github.com/B4PT0R/pkgmngr",
        "Documentation": "https://github.com/B4PT0R/pkgmngr#readme",
    },
    package_data={
        "pkgmngr": ["templates/*.txt", "*.md"],
    },
)