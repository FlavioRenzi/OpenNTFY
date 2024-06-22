from setuptools import setup, find_packages

setup(
    name='OpenNTFY',
    version='0.1.0',
    author='Flavio Renzi',
    author_email='flavioinv@gmail.com',
    description='A simple command line tool to send notifications to your telegram bot',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/FlavioRenzi/OpenNTFY',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'asyncio',
        'textual',
        'python-telegram-bot',
        'pyte',
    ],
    entry_points={
        'console_scripts': [
            'OpenNTFY=OpenNTFY.OpenNTFY:main',
        ],
    },
)
