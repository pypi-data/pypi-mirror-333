from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    page_description = f.read()

setup(
    name="bank_system-aliceferreiracodes",
    version="0.0.1",
    author="aliceferreiracodes",
    description="A bank system using Python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aliceferreiracodes/bank-system",
    packages=find_packages(),
    python_requires='>=3.10'
)
