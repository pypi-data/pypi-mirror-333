from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)  # Run the standard install
        os.system("python -m MLEssentials.post_install")  # Execute the post-install script

setup(
    name="MLEssentials",
    version="1.2",
    author="Rohit Kosamkar",
    author_email="rohitkosamkar97@gmail.com",
    description="A comprehensive toolkit that streamlines machine learning development by installing all essential libraries in a single command.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rohit180497/MLToolkit",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "machine learning", "ML toolkit", "data science", "AI libraries", "python ML", 
        "numpy", "pandas", "scikit-learn", "xgboost", "deep learning", "data analysis"
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "scipy",
        "nltk",
        "plotly",
        "matplotlib",
        "seaborn",
        "pydot",
        "statsmodels",
        "spacy",
        "fastapi",
        "streamlit",
        "polars",
        "xgboost",
        "lightgbm",
        "catboost",
        "pattern",
        "selenium",
        "pandasql",
        "mysql-connector-python",
        "pyodbc",
        "pydantic",
        "azure-identity",
        "flask",
        "beautifulsoup4",
        "SQLAlchemy",
        "pyyaml",
        "tqdm",
        "openpyxl",
        "pyarrow",
        "networkx"
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "mlessentials-postinstall=MLEssentials.post_install:print_imports"
        ]
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    project_urls={
        "Bug Tracker": "https://github.com/rohit180497/MLToolkit/issues",
        "Documentation": "https://github.com/rohit180497/MLToolkit#readme",
        "Source Code": "https://github.com/rohit180497/MLToolkit"
    },
)
