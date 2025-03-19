from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="errorslib",  # Lowercase, no spaces
    version="1.2",
    packages=find_packages(),  # Auto-detects 'elib'
    install_requires=[],  # List dependencies if needed
    author="wowsuchdog",
    author_email="kirboistic@gmail.com",
    description="Why would you use this?",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manOnWebs/errorslib",  # Replace with your actual GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    License="MIT License",
    python_requires=">=3.6",  # Ensures compatibility
)
