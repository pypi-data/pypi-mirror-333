#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='oss-upload-utils',  # 项目的名称,pip3 install get-time
    version='0.0.2',  # 项目版本
    author='MindLullaby',  # 项目作者
    author_email='3203939025@qq.com',  # 作者email
    # url='',  # 项目代码仓库
    description='oss文件上传',  # 项目描述
    packages=['oss_upload_utils'],  # 包名
    install_requires=[
        "beautifulsoup4",
        "ftfy",
        "html2text",
        "loguru",
        "oss2",
        "rarfile",
        "setuptools"
    ],
    # entry_points={
    #     'console_scripts': [
    #         'get_time=get_time:get_time', # 使用者使用get_time时,就睡到get_time项目下的__init__.py下执行get_time函数
    #         'get_timestamp=get_time:get_timestamp',
    #         'timestamp_to_str=get_time:timestamp_to_str',
    #         'str_to_timestamp=get_time:str_to_timestamp',
    #     ]
    # } # 重点
)
