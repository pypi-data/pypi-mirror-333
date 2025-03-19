from distutils.core import  setup
import setuptools
packages = ['XwsLibrary']# 唯一的包名，自己取名
setup(name='XwsLibrary',
	version='1.1',
	author='XiaoWang',
    description="wow~高级",
    author_email='wzxddzyj1@outlook.com',
    packages=packages, 
    package_dir={'requests': 'requests'},)
