from setuptools import setup, find_packages
from setuptools.command.sdist import sdist
import os
import subprocess

class UploadCommand(sdist):
    """Custom command to upload the package to PyPI"""
    def run(self):
        # Create the distribution files
        subprocess.check_call(['python', 'setup.py', 'sdist', 'bdist_wheel'])

        # Upload the distribution files
        subprocess.check_call(['twine', 'upload', 'dist/*'])

        # Let the original sdist command run
        sdist.run(self)

setup(
    name="errorprinter",
    version="0.1",
    packages=find_packages(),
    description="A Python package to print errors beautifully with detailed explanations.",
    author="Hobe",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    cmdclass={
        'upload': UploadCommand,
    }
)
