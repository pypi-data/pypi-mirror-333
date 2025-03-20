import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "xregion-ssm-parameter-reader",
    "version": "0.0.7",
    "description": "xregion-ssm-parameter-reader",
    "license": "Apache-2.0",
    "url": "https://github.com/cmorgiaorg/xregion-ssm-parameter-reader.git",
    "long_description_content_type": "text/markdown",
    "author": "Claudio Morgia<214524+cmorgia@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cmorgiaorg/xregion-ssm-parameter-reader.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "xregion-ssm-parameter-reader",
        "xregion-ssm-parameter-reader._jsii"
    ],
    "package_data": {
        "xregion-ssm-parameter-reader._jsii": [
            "xregion-ssm-parameter-reader@0.0.7.jsii.tgz"
        ],
        "xregion-ssm-parameter-reader": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.9",
    "install_requires": [
        "aws-cdk-lib>=2.183.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.109.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
