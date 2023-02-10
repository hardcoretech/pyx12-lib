import setuptools

setuptools.setup(
    name="pyx12lib",
    version="0.2",
    author="CJHwong",
    author_email="pypi@hardcoretech.co",
    url="https://github.com/hardcoretech/pyx12-lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"pyx12lib": "pyx12lib"},
    packages=setuptools.find_packages(),
    install_requires=[
        "six",
    ],
    python_requires=">=3.6",
)
