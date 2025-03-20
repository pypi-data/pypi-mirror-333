from setuptools import setup, find_packages

# Read long description from README.md if available
long_description = ""
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "An unofficial API for Passio Go."

# Define setup configuration
setup(
    name="PassioGo_updated",
    version="0.2.2",
    description="An unofficial API for Passio Go",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Andrei Thuler",
    author_email="info@andreithuler.com",
    url="https://github.com/athuler/PassioGo",
    packages=find_packages(),  # Automatically finds all Python packages
    install_requires=[
        "requests"  # ✅ Directly specify required dependencies
    ],
    project_urls={
        "Documentation": "https://passiogo.readthedocs.io/",
        "GitHub": "https://github.com/athuler/PassioGo",
        "Sponsor": "https://github.com/sponsors/athuler",
        "Changelog": "https://github.com/athuler/PassioGo/blob/main/CHANGELOG.md",
    },
    python_requires=">=3.7",  # Ensures compatibility with Python 3.7+
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
