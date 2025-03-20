from setuptools import setup, find_packages

setup(
    name="speedportonetop",
    version="1.0.1", 
    packages=find_packages(),
    install_requires=[
        "flask", 
    ],
    author="speedportonetop",
    description="A simple web terminal running on port 8000",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/speedportonetop", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
