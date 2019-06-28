from setuptools import setup, find_packages

setup(
    name='hue',
    version='0.1',
    py_modules=['hue'],
    install_requires=[
        'Click',
        'colorama',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        hue=hue:cli
    ''',
)