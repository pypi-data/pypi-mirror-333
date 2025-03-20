import setuptools
import os

# Read the README.md file for the long description
with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mesh-sdk",
    version="1.3.1",
    author="Mesh Team",
    author_email="info@mesh.com",
    description="Python SDK for the Mesh API with improved authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meshapi/mesh-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "keyring>=21.0.0",
        "python-dotenv>=0.15.0",
    ],
    entry_points={
        "console_scripts": [
            "mesh-auth=mesh_sdk.auth_cli:main",
        ],
    },
)