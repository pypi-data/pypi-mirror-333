from setuptools import setup

__version__ = "1.0.2"
__copyright__ = "Copyright 2025, Aaron Edwards"
__license__ = "MIT"

with open('README.md') as f:
    long_description = f.read()

setup(name='bod',
      version=__version__,
      description='Text Blob and Object Dumper',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ebob9/bod',
      author='Aaron Edwards',
      author_email='bod-util@ebob9.com',
      license=__license__,
      install_requires=[
            'beautifulsoup4',
            'requests'
      ],
      packages=['bod'],
      classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "Operating System :: OS Independent"
      ]
      )