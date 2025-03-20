from setuptools import setup, find_packages

setup(
    name='ChronoFlex',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pytz',
        'python-dateutil',
        'babel',
    ],
    author='Khotso Tsoaela',
    author_email='khotso.s.tsoaela@gmail.com',
    description='A Python package for enhanced date and time formatting, localization, time zone conversion, and scheduling.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ktsoaela/ChronoFlex',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)