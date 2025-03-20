from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="auto-ml-processor",
    version="0.1.2",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated machine learning preprocessing and modeling tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/auto-ml-processor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "scikit-learn>=0.22.0",
        "xgboost>=1.0.0",
        "joblib>=0.14.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "full": [
            "datasets>=2.0.0",  # For Hugging Face datasets
            "kaggle>=1.5.0",    # For Kaggle datasets
            "opendatasets>=0.1.0", # For additional data sources
        ],
    },
)