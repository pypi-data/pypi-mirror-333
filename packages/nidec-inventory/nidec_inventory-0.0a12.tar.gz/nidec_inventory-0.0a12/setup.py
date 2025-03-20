from setuptools import setup, find_packages

setup(
    name="nidec-inventory",
    version="0.0a12",
    description="Nidec Unidrive M motor control drives inventory generator.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Carlos Alonso Martín",
    author_email="cam.codeweaver@gmail.com",
    url="https://github.com/carlosalma/nidec-inventory",
    license="MIT License",
    packages=find_packages(),
    package_data={'': ["*.yaml"]}
)