from setuptools import setup, find_packages

setup(
    name="aptai",
    version="1.1.0",
    author="Teck",
    author_email="teckdegen@gmail.com",
    description="Aptos AI-powered DeFi and NFT toolkit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Teckdegen/aptai",
    packages=find_packages(),
    install_requires=[
        "requests",
        "aptos_sdk",
        "groq",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
