from setuptools import setup, find_packages

setup(
    name="pptools",
    version="0.1.0",
    author="PPTools Contributors",
    author_email="your.email@example.com",
    description="一个全面的Python工具包，用于自动化测试和日常开发工作",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://gitee.com/dyliujun/pptools.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "pyyaml",
        "openpyxl",
        "pymongo",
        "redis",
        "pandas",
        "adbutils",
        "psutil"
    ],
    extras_require={
        "database": ["pymongo", "pymysql", "redis"],
        "dev": ["pytest", "black", "isort", "mypy", "flake8", "build", "twine"]
    }
)