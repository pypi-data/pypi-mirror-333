from setuptools import setup, find_packages

setup(
    name="onyxcloud",
    version="1.12.0",
    description="Python package for the OnyxCloud CTF challenge. Part 1",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    author="CTFByte",
    author_email="dev@ctfbyte.com",
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    package_data={'onyxcloud': ['onyxcloud.chat.py', 'onyxcloud.Utils.py', 'onyxcloud.__init__.py', 'model/modelpt']},
    include_package_data=True,
    install_requires=[
        "torch==2.6.0",
        "numpy==2.1.3",
        "matplotlib==3.9.3",
        "ctfbyte-colorama==0.5.1",
    ],
    entry_points={
        "console_scripts": [
            "onyxcloud=onyxcloud.main:main",
        ],
    },
)

