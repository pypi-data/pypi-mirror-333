from setuptools import setup, find_packages
from setuptools.command.sdist import sdist
import subprocess
import os

class UploadCommand(sdist):
    """Custom command to upload the package to PyPI"""
    def run(self):
        # Make sure we have the necessary files in the current directory
        subprocess.check_call(['python', 'setup.py', 'sdist', 'bdist_wheel'])

        # Change the directory to the current working directory to avoid extra dist folder
        os.chdir(os.getcwd())

        # Upload the distribution files using twine from the current folder
        subprocess.check_call(['twine', 'upload', '*.tar.gz', '*.whl'])

        # Let the original sdist command run
        sdist.run(self)

setup(
    name="errorprinter",
    version="0.3",
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
