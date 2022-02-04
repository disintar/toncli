import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tncli",
    version="0.0.42",
    author="Andrey Tvorozhkov",
    author_email="andrey@head-labs.com",
    description="Easy to use CLI for fift / func projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/disintar/tncli",
    project_urls={
        "Bug Tracker": "https://github.com/disintar/tncli/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apple Public Source License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'tncli = tncli.main:main',
        ],
    }
)
