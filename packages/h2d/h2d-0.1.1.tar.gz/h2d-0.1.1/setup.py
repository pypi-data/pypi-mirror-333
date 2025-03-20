from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="h2d",
    version="0.1.1",
    author="zzzyansong",
    author_email="i@zhuyansong.com",
    description="轻松将您的html转为docx格式",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zzzyansong/h2d",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where='.', exclude=(), include=('*',)),
    python_requires=">=3.6",
    install_requires=[
        'python-docx>=0.8.11',
        'requests>=2.28.0',
        'beautifulsoup4>=4.12.0',
        'cssutils>=2.7.1',
    ],
)