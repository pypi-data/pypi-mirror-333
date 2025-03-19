from setuptools import setup

setup(
    name='dummygen-cli',
    version='0.1.2',
    entry_points={
        'console_scripts': [
            'dummygen-cli=dummygen_cli:main',
        ],
    },
    install_requires=[
        'rich',
    ],
    author='Ervan Kurniawan',
    author_email='ervankurniawan41@gmail.com',
    description='A simple tool to generate dummy files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/karvanpy/dummygen-cli',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)
