from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup (
    name='snl_exp_regression_quality',
    version='0.1.2',
    license='MIT',
    description='simple no linear regression quality (Exponential)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author= 'EdelH, Aplatag',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'snl_regression_quality': ['data/*'],
        
    },

    install_requires = ['numpy','pandas','scikit-rf','matplotlib','scipy'],

    url='https://github.com/aplatag/project_SNL_regression_quality'
)