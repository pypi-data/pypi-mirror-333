# _*_ coding: utf-8 _*_
# @Time : 2023/5/19
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :

from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).resolve().parent
README = (here / "README.md").read_text(encoding="utf-8")

excluded_packages = ["tests", "tests.*"]

# this module can be zip-safe if the zipimporter implements iter_modules or if
# pkgutil.iter_importer_modules has registered a dispatch for the zipimporter.
try:
    import pkgutil
    import zipimport

    zip_safe = (
            hasattr(zipimport.zipimporter, "iter_modules")
            or zipimport.zipimporter in pkgutil.iter_importer_modules.registry.keys()
    )
except AttributeError:
    zip_safe = False

requires = [
    "async-timeout>=5.0.1",
    "DBUtils>=3.1.0",
    "dnspython>=2.7.0",
    "loguru>=0.7.3",
    "pymongo>=4.11.1",
    "PyMySQL>=1.1.1",
    "redis>=5.2.1"
]

setup(
    name="DigiCoreOdbc",
    version="1.0.0",
    description="DigiCoreOdbc是一个基于Python的数字化支持部数据库连接使用的第三方库，旨在为数据处理和开发提供完备的工具集和服务。",
    long_description=README,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="DigiCoreOdbc是服务于道诚集团数字化支持部的自建第三方库项目",
    author="yarm",
    author_email="yangyang@doocn.com",
    license="MIT License",
    packages=find_packages(exclude=excluded_packages),
    install_requires=requires,
    platforms=["any"],
    zip_safe=zip_safe,
    python_requires=">=3.8",
)
