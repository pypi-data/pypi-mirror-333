from setuptools import setup, find_packages

setup(
    name='Shivam-STT',
    version='0.1',
    author='Shivam',
    author_email='shivam.2011.3285@gmail.com',
    description='this is speech to text package created by shivam'
)
packages = find_packages(),
install_requirements= [
    'selenium',
    'webdriver_manager'
]
