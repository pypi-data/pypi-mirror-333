import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reflec",
    version="0.0.1",
    author="enpotid",
    description="Deep learning framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enpotid/reflec",
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy==2.0.2",
    ],
    classifiers=[ 
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)
