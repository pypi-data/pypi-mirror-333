import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "transitgw-peering-accepter",
    "version": "0.0.19",
    "description": "transitgw-peering-accepter",
    "license": "Apache-2.0",
    "url": "https://github.com/cmorgiaorg/transitgw-peering-accepter.git",
    "long_description_content_type": "text/markdown",
    "author": "Claudio Morgia<214524+cmorgia@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cmorgiaorg/transitgw-peering-accepter.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "transitgw-peering-accepter",
        "transitgw-peering-accepter._jsii"
    ],
    "package_data": {
        "transitgw-peering-accepter._jsii": [
            "transitgw-peering-accepter@0.0.19.jsii.tgz"
        ],
        "transitgw-peering-accepter": [
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
