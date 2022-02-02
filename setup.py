import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fift-cli",
    version="0.0.1",
    author="Andrey Tvorozhkov",
    author_email="andrey@head-labs.com",
    description="Easy to use CLI for fift / func projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/disintar/fift-cli",
    project_urls={
        "Bug Tracker": "https://github.com/disintar/fift-cli/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: WTFPL License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'fift-cli = fift_cli.main:main',
        ],
    }
)
