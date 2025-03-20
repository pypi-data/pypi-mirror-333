import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-cloudformation-netapp-fsxn-snapmirror",
    "version": "1.3.0.a7",
    "description": "FSx for ONTAP offers SnapMirror for efficient data replication between file systems, aiding in data protection, disaster recovery, and long-term retention. To use SnapMirror, set up cluster peering and SVM peering between the source and target FSx for ONTAP file systems. Once activated, you need a preview key to consume this resource. Please reach out to Ng-fsx-cloudformation@netapp.com to get the key. To use this resource, you must first create the Link module.",
    "license": "Apache-2.0",
    "url": "https://github.com/NetApp/NetApp-CloudFormation-FSx-ONTAP-provider",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/cdk-cloudformation.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_cloudformation_netapp_fsxn_snapmirror",
        "cdk_cloudformation_netapp_fsxn_snapmirror._jsii"
    ],
    "package_data": {
        "cdk_cloudformation_netapp_fsxn_snapmirror._jsii": [
            "netapp-fsxn-snapmirror@1.3.0-alpha.7.jsii.tgz"
        ],
        "cdk_cloudformation_netapp_fsxn_snapmirror": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.182.0, <3.0.0",
        "constructs>=10.4.2, <11.0.0",
        "jsii>=1.108.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
