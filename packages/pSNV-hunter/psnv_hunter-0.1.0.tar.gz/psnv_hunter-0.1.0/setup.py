from setuptools import setup, find_packages

setup(
    name="pSNV-hunter",  # Your package name
    version="0.1.0",  # Update this for each release
    author="Nicholas Abad",
    author_email="nicholas.a.abad@gmail.com",
    description="A comprehensive visualization tool for analyzing pSNVs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nicholas-abad/pSNV-hunter",
    packages=find_packages(where="src"),  # Finds packages inside 'src/'
    package_dir={"": "src"},  # Defines base package directory
    install_requires=[
        "dash",
        "dash-bio",
        "numpy",
        "pandas",
        "plotly",
        "dash-bootstrap-components",
        "dash-table",
        "notebook",
        "matplotlib",
        "tqdm",
        "scikit-learn",
        "scipy"
    ],
    entry_points={
        "console_scripts": [
            "pSNV-hunter=pSNV_hunter.run_visualization_tool:main",  # Exposes CLI command
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)