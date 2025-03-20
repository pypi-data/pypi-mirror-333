from setuptools import setup, find_packages

setup(
    name='flask-mvc-core',
    description='A simple MVC package for Flask',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Célio Junior',
    author_email='profissional.celiojunior@gmail.com',
    url='https://github.com/celiovmjr/flask-mvc-core',
    packages=find_packages(include=['flask_mvc_core', 'flask_mvc_core.*']),
    include_package_data=True,
    install_requires=['Flask>=3.0', 'werkzeug>=2.0',],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
