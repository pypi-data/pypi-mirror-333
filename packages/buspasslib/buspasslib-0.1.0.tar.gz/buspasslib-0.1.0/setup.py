from setuptools import setup, find_packages

setup(
  name='buspasslib',
  version='0.1.0',
  description='This is a simple Python package that prints the bus pass number of user.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Anusha-x23420065@student.ncirl.ie',
  author_email='x23420065@student.ncirl.ie',
  classifiers=[
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
],
  keywords='buspasslib', 
  packages=find_packages(),
  python_requires=">=3.6"
)
