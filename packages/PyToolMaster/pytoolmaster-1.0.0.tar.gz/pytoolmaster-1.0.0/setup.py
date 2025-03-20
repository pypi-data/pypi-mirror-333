from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="PyToolMaster",
    version="1.0.0",
    author="Shiboshree Roy",
    author_email="shiboshreeroy169@gamil.com",
    description="A Swiss Army knife for developers with text summarization, ASCII art, task automation, math tools, and error handling.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shiboshreeroy/PyToolMaster",
    packages=find_packages(),
    install_requires=[
        "sumy",
        "Pillow",
        "schedule",
        "sympy",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)