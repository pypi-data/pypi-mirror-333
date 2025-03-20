from setuptools import setup, find_packages

setup(
    name="speed-port",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "flask",
    ],
    entry_points={
        "console_scripts": [
            "run.8000=speed_port.server:run_8000",
        ],
    },
    author="speed",
    description="A simple web shell on port 8000",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
