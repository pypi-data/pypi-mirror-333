from setuptools import setup, find_packages

setup(
    name="code-qfire",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "termcolor",
    ],
    entry_points={
        "console_scripts": [
            "code-qfire=code_qfire.main:main",
        ],
    },
    author="Your Name",
    author_email="your-email@example.com",
    description="A lightweight code optimization tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code-qfire",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
