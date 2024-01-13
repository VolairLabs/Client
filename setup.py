#!/usr/bin/python3
# -*- coding: utf-8 -*-

from setuptools import setup

with open("requirements.txt") as fp:
    install_requires = fp.read()
setup(
    name="volair",
    version="0.34.3",
    description="""Magic Cloud Layer""",
    long_description="".join(open("README.md", encoding="utf-8").readlines()),
    long_description_content_type="text/markdown",
    url="https://github.com/Volair/Volair",
    author="Volair",
    author_email="onur.atakan.ulusoy@volair.co",
    license="MIT",
    packages=["volair", "volair.remote", "volair.remote.localimport"],
    install_requires=install_requires,
    entry_points={
        "console_scripts": ["volair=volair.remote.interface:Volair_CLI"],
    },
    python_requires=">=3.6",
    zip_safe=False,
)
