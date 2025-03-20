from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="filesync-guardian",
    version="0.1.1",
    author="Biswanath Roul",
    description="A robust file synchronization and backup library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/biswanathroul/filesync-guardian",
    project_urls={
        "Bug Tracker": "https://github.com/biswanathroul/filesync-guardian/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Archiving :: Mirroring",
        "Topic :: Utilities",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "cryptography>=36.0.0",
    ],
    keywords=["file", "sync", "backup", "synchronization", "versioning", "encryption"],
)