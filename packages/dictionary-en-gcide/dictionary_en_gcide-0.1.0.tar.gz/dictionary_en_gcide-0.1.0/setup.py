from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="dictionary_en_gcide",
    version="0.1.0",
    author="Rafael Lins",
    author_email="leafarlins@gmail.com",
    description="A Python module for english dictionary lookup, based on gcide",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leafarlins/dictionary_en_gcide",
    packages=find_packages(),
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify Python version compatibility
    install_requires=[
        # Add dependencies if needed
    ]
)