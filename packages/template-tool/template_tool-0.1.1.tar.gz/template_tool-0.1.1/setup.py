from setuptools import setup

setup(
name='template_tool',
version='0.1.1',
description='A package for manage python templates',
author='sk2011se',
author_email='eatebarisajjad@gmail.com',
packages=['template_tool', 'template_tool.colorization', 'template_tool.actions'],
install_requires=[
'colorama',
'argparse'
]
)