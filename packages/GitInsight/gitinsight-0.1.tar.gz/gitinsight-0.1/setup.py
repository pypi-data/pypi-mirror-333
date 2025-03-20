from setuptools import setup, find_packages

setup(
    name='GitInsight',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'gitpython',
        'click',
        'matplotlib',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'gitinsight=gitinsight.cli:analyze',
        ],
    },
    author='Khotso Tsoaela',
    author_email='khotso.s.tsoaela@gmail.com',
    description='A CLI tool to analyze Git repositories and provide insights.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ktsoaela/GitInsight',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)