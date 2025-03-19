from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="galamo",
    version="1.0.6",
    author="Jashanpreet Singh Dingra",
    author_email="astrodingra@gmail.com",
    description="A Python package for classifying galaxy morphologies using deep learning.",
    long_description=long_description,  # Use the content from README.md
    long_description_content_type="text/markdown",  # Markdown format
    url="https://github.com/jdingra11/galamo",
    project_urls={
        "Model Download (Zenodo)": "https://doi.org/10.5281/zenodo.15002609"
    },
    packages=find_packages(),
    package_data={
        "galamo": ["model.keras", "encoder.pkl"],
    },
    include_package_data=True,
    install_requires=[
        "tensorflow",
        "numpy",
        "opencv-python",
        "joblib",
        "requests"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    python_requires=">=3.7",
)
