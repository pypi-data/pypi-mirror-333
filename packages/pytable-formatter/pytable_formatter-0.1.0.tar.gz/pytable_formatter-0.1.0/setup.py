from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytable-formatter",
    version="0.1.0",
    author="Biswanath Roul",
    author_email="authorbiswanath@gmail.com",
    description="Advanced table formatting for terminal output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/biswanathroul/pytable-formatter",
    project_urls={
        "Bug Tracker": "https://github.com/biswanathroul/pytable-formatter/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    keywords="table, terminal, cli, formatting, console",
)