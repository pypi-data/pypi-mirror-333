from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aitokencount",
    version="0.1.1",
    author="Harry Wang",
    author_email="harryjwang@gmail.com",
    description="Count AI tokens in files and directories using tiktoken",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harrywang/aitokencount",
    project_urls={
        "Bug Tracker": "https://github.com/harrywang/aitokencount/issues",
        "Source Code": "https://github.com/harrywang/aitokencount",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "tiktoken>=0.5.2",
    ],
    entry_points={
        "console_scripts": [
            "aitokencount=aitokencount.cli:main",
        ],
    },
)
