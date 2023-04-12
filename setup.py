from setuptools import setup, find_packages

setup(
    name="aiia",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "PyYAML",
        "playwright",
        "readability-lxml",
    ],
    entry_points={"console_scripts": ["aiia = aiia.cli:main"]},
    classifiers=[
        "Development Status :: Alpha",
        "Intended Audience :: e/acc",
        "License :: OSI Approved :: MIT License",
    ],
    extras_require={
        "dev": [
            "black",
            "pytest",
        ],
    },
)
