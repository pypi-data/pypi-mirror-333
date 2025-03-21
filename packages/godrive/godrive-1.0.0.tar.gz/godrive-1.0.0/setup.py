from setuptools import setup
import os

setup(
    name="godrive",
    version="1.0.0",
    packages=["godrive"],  # Python package (needed for pip)
    include_package_data=True,
    install_requires=[],  # No dependencies needed
    data_files=[("bin", ["bin/godrive", "bin/godrive_upload"])],  # Mark as binaries
    zip_safe=False,
)

