from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="repo-to-one-file",
    version="1.0.4",
    author="tonypls",
    author_email="tony@appy.co.nz",
    description="A tool to consolidate repository files into a single file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonypls/repo-to-one-file",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        # List your project dependencies here
    ],
    entry_points={
    "console_scripts": [
        "repo-to-one-file=repo_to_one_file.__main__:main",
    ],
},
)