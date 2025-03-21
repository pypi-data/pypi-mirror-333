from setuptools import setup, find_packages

setup(
    name='structured-response',  # Package name
    version='0.1.0',  # Initial release version
    packages=find_packages(),  # Automatically discover all packages in the directory
    install_requires=['Flask>=3.0.0,<4.0'],  # Dependencies needed to install the package
    description='A simple package to generate structured HTTP responses with trace ID.',
    author='Rohaan Nadeem',
    author_email='rohaan@rohaannadeem.com',
    url='https://github.com/rohaan2614/structured-response',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)