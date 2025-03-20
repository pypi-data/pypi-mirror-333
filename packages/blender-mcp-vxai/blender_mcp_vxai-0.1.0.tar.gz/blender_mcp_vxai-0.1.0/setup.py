#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# Package definition
setup(
    name="blender_mcp_vxai",
    version="0.1.0",
    packages=["blender_mcp_vxai", "blender_mcp_vxai.server", "blender_mcp_vxai.addon"],
    include_package_data=True,
    install_requires=[
        "Pillow",
        "mcp>=1.3.0",
    ],
    entry_points={
        "console_scripts": [
            "blender-mcp-vxai=blender_mcp_vxai.server.server:main",
        ],
    },
) 