from setuptools import setup

setup(
    name='papercast',
    version='0.1',
    py_modules=['papercast'],
    install_requires=[
        'click',
        'spacy',
        'en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.0.0/en_core_web_sm-2.0.0.tar.gz',
        'beautifulsoup4',
        'mutagen'
    ],
    entry_points='''
        [console_scripts]
        papercast=papercast.scripts.papercast:papercast
    ''',
)
