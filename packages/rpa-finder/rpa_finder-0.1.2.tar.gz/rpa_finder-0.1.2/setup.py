from setuptools import setup, find_packages

setup(
    name='rpa_finder',
    version='0.1.2',
    packages=find_packages(),
    description='A python package to find robust perfect adaptation of chemical reaction networks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yuji Hirono, Ankit Gupta',
    author_email='yuji.hirono@gmail.com',
    url='https://github.com/yhirono/RPAFinder',
    install_requires=[
        'numpy>=1.25.2',
        'python_libsbml>=5.20.2',
        'scipy>=1.13.0',
        'setuptools>=58.0.4',
        'sympy>=1.12',
        'matplotlib>=3.8.2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
