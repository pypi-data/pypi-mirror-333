from setuptools import setup, find_packages

setup(
    name="omkarbhosale-upi-qr",
    version="1.1.0",
    author="Omkar Bhosale",
    author_email="omkarbhosale5484@email.com",
    description="Generate UPI QR codes with specified amounts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/0mkarBhosale07/python-upi-qr",
    packages=find_packages(),
    install_requires=[
        "qrcode[pil] >=7.4.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
