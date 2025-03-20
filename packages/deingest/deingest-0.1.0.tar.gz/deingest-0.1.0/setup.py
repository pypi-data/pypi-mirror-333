from setuptools import setup, find_packages

setup(
    name="deingest",
    version="0.1.0",
    description="Reverse a gitingest digest file to restore the original repository structure.",
    author="Javad Razi",
    author_email="javad.razigiglou@gmail.com",
    url="https://github.com/jrazi/deingest",
    packages=find_packages(),
    install_requires=["click>=7.0"],
    entry_points={
        "console_scripts": [
            "deingest=deingest.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
