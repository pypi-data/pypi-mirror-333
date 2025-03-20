from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pipli",
    version="1.0.3",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pipli=pipli.main:main"
        ]
    },
    author="Rahul Paul",
    author_email="devnull90210@gmail.com",
    description="A CLI tool that automatically installs missing Python dependencies and runs the given command.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paulrahul/pipli",
    project_urls={
        "Bug Tracker": "https://github.com/paulrahul/pipli/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
