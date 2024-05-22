from setuptools import setup, find_packages

setup(
    name='mkToHtml',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'mkToHtml = main:main',  # main.py 内の main 関数を指す
        ],
    },
)
