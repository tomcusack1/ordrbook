from distutils.core import setup
import setuptools


setup(name='ordrbook',
      version='0.0.1',
      author='Tom Cusack-Huang',
      author_email='tom@cusack-huang.com',
      packages=['ordrbook'],
      url='https://github.com/tomcusack1/ordrbook',
      download_url='https://github.com/tomcusack1/ordrbook/archive/v_001.tar.gz',
      description='Limit Order Book',
      install_requires=['bintrees', 'blkchn'])
