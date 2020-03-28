import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="package_visualization_tool_PE-emse2020", # Replace with your own username
    version="0.0.1",
    author="Ecole des Mines de Saint-Etienne 2020",
    author_email="khatibomar3@gmail.com",
    description="Data Visualization for metrology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)