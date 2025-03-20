# setup.py

from setuptools import setup, find_packages

setup(
    name="fourtest",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "fourtest"
    ],
        entry_points={
        "console_scripts": [
            "fourtest-api=fourtest.api:run"
        ]
    },
    author="fourchains",
    description="A simple example fourtest",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    tests_require=["pytest"],
)
