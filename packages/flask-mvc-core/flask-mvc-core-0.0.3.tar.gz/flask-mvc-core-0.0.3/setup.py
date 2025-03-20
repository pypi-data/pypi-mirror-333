from setuptools import setup, find_packages

setup(
    name='flask-mvc-core',
    version='0.0.3',
    description='A simple MVC package for Flask',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Célio Junior',
    author_email='profissional.celiojunior@gmail.com',
    packages=find_packages(),
    install_requires=['Flask>=3.0'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
