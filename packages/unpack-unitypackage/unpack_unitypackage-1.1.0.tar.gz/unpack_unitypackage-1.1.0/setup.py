#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="unpack-unitypackage",
    version="1.1.0",
    description="解压和提取Unity包文件的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="xiayangqun",
    author_email="xyq377x@gmail.com",
    # 移除GitHub仓库URL或将其设为空
    # url="https://github.com/yourusername/unpack-unitypackage",
    packages=find_packages(),
    py_modules=["unpack_unitypackage"],
    install_requires=[
        "unitypackage_extractor",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    scripts=["unpack_unitypackage.py"],
    entry_points={
        "console_scripts": [
            "unpack_unitypackage=unpack_unitypackage:main",
            "unpack-unitypackage=unpack_unitypackage:main",
        ],
    },
) 