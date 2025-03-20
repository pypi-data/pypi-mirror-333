import setuptools

exec(open("tcpb_trio/_version.py").read())

setuptools.setup(
    name="tcpb-trio",
    version=__version__,
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "protobuf >= 3.20",
        "trio",
        "numpy",
    ],
    extras_require={
        "dev": [
            "grpcio-tools",
            "black",
            "pre-commit",
            "build",
            "twine",
        ],
    },
    tests_require=[],
)
