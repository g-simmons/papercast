from setuptools import setup

setup(
    name='papercast',
    version='0.1',
    py_modules=['papercast'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        papercast=papercast.scripts.papercast:papercast
    ''',
)
