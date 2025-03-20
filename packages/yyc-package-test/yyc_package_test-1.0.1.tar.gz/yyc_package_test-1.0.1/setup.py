# from distutils.core import setup
from setuptools import setup

# 读取文件内容
def readme_file():
    with open("README.rst", encoding='utf-8') as rf:
        return rf.read()

setup(name="yyc_package_test", version="1.0.1", description="this is yyc's first package ah",
      packages=["yyc_package"], py_modules=["Tool"], author="yyc",
      long_description=readme_file())