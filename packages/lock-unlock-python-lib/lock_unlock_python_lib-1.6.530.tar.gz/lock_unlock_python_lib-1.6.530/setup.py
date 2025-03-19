from setuptools import setup, find_packages

setup(
    name="lock-unlock-python-lib",
    version="1.6.530",
    author="razzycode",
    author_email="nebisaylan14@gmail.com",
    description="(en) A simple encryption and decryption library for folders (tr) Klasörler için basit bir şifreleme ve şifre çözme kütüphanesi",
    long_description=open("README-tr.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/razzy-code/lock-unlock-python-lib",
    packages=find_packages(),
    install_requires=["pycryptodome", "psutil"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
