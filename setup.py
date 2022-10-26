import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imagepreprocessors",  # Replace with your own username
    version="0.0.1",
    author="Tuhin Mallick",
    author_email="tuhin.mllk@gmail.com",
    description="Service for demonstration of Albumentations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tuhinmallick/imagepreprocessor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
