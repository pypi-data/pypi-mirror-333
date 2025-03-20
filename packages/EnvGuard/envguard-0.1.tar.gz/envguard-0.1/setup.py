from setuptools import setup, find_packages

setup(
    name='EnvGuard',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'envguard=envguard.cli:validate_env',
        ],
    },
    author='Khotso Tsoaela',
    author_email='khotso.s.tsoaela@gmail.com',
    description='A tool to check for missing or incorrect environment variables in .env files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ktsoaela/EnvGuard',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)