from setuptools import setup

with open("README.md", "r") as desc_file:
    long_description = desc_file.read()

setup(
  name = 'datasize',
  packages = ['datasize'],
  version = '1.0.0',
  description = 'Python integer subclass to handle arithmetic and formatting of integers with data size units',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Jeremy McMillan',
  author_email = 'jeremy.mcmillan@gmail.com',
  url = 'https://github.com/aphor/datasize',
  download_url = 'https://github.com/aphor/datasize/tarball/1.0.0',
  keywords = ['data', 'units', 'parser', 'formatter'],
  classifiers = [],
)
