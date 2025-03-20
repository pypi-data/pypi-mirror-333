from setuptools import setup, find_packages

setup(
    name="kingpepe-sdk",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "bitcoinlib"
    ],
    description="SDK for King Pepe (KPEPE) Blockchain",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/YOUR_USERNAME/kingpepe-sdk",
)
