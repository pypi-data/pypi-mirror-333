from setuptools import setup, find_packages

setup(
  name='artexhibitionlib',
  version='0.2.0',
  description='This is a simple Python package that prints the bus pass details of user.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Nithin Bonagiri',
  author_email='x24137430@student.ncirl.ie',
  classifiers=[
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
],
  keywords='artexhibitionlib', 
  packages=find_packages(),
  python_requires=">=3.6"
)
