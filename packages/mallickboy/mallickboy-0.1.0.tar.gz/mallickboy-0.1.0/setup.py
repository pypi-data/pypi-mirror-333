from setuptools import setup, find_packages
from setuptools.command.install import install
import sys

class CustomInstallCommand(install):
    def run(self):
        # Show a custom message during installation
        print("*****************************************************")
        print("Message : This mallickboy library has been developed by Tamal Mallick (github/mallickboy)")
        print("""Libraries: 
              1. runtime    (decorator to know runtime of any program)\n
              2. rle        (Run-Length Encoding aaabbc to a3b2c)"""
             )
        print("Installing my custom library...")
        print("*****************************************************")
        sys.stdout.flush()
        # install.run(self)
        install.run(self)

setup(
    name='mallickboy',
    version='0.1.0',
    description="This is my custom library for python",
    long_description=""" 
        *****************************************************
        Message : This mallickboy library has been developed by Tamal Mallick (github/mallickboy)

        Modules included:
        1. runtime - Decorator to measure the runtime of any program
        2. rle - Run-Length Encoding (aaabbc → a3b2c)

        *****************************************************
        """,
    long_description_content_type="text/plain",
    author="Tamal Mallick",
    author_email="contact@mallickboy.com",
    packages= find_packages(),
    url="https://github.com/mallickboy",
    license="Free to use and open for customization if provided appropriate credit to the author.",
    install_requires=[  # dependencies required for my package
        # "setuptools" #  to setup the module
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
    entry_points={
        "console_scripts": [
            "mallickboy= mallickboy:hellow"
            ],
    },
)
# Name: mallickboy
# Version: 0.0.3
# Summary: 
# Home-page: 
# Author: 
# Author-email: 
# License: 
# Location: C:\Users\tamal\AppData\Roaming\Python\Python313\site-packages
# Requires: 
# Required-by:

### takes

#     name: str = ...,
#     version: str = ...,
#     description: str = ...,
#     long_description: str = ...,
#     long_description_content_type: str = ...,
#     author: str = ...,
#     author_email: str = ...,
#     maintainer: str = ...,
#     maintainer_email: str = ...,
#     url: str = ...,
#     download_url: str = ...,
#     packages: list[str] = ...,
#     py_modules: list[str] = ...,
#     scripts: list[str] = ...,
#     ext_modules: Sequence[Extension] = ...,
#     classifiers: list[str] = ...,
#     distclass: type[Distribution] = ...,
#     script_name: str = ...,
#     script_args: list[str] = ...,
#     options: Mapping[str, Incomplete] = ...,
#     license: str = ...,
#     keywords: list[str] | str = ...,
#     platforms: list[str] | str = ...,
#     cmdclass: Mapping[str, type[Command]] = ...,
#     data_files: list[tuple[str, list[str]]] = ...,
#     package_dir: Mapping[str, str] = ...,
#     obsoletes: list[str] = ...,
#     provides: list[str] = ...,
#     requires: list[str] = ...,
#     command_packages: list[str] = ...,
#     command_options: Mapping[str, Mapping[str, tuple[Incomplete, Incomplete]]] = ...,
#     package_data: Mapping[str, list[str]] = ...,
#     include_package_data: bool = ...,
#     libraries: list[tuple[str, _BuildInfo]] = ...,
#     headers: list[str] = ...,
#     ext_package: str = ...,
#     include_dirs: list[str] = ...,
#     password: str = ...,
#     fullname: str = ...,
