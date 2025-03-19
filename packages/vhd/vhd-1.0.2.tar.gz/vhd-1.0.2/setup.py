from setuptools import setup, find_packages

setup(
    name='vhd',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        # 依赖列表
    ],
    author='ZhongYang',
    author_email='19865697458@163.com',
    description='VHD操作库',
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://gitee.com/yangyingyun/vhd',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)