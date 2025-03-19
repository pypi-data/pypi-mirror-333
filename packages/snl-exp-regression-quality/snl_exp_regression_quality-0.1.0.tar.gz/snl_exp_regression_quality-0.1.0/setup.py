from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup (
    name='snl_exp_regression_quality',
    version='0.1.0',
    license='MIT',
    description='simple no linear regression quality (Exponential)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author= 'EdelH, Aplatag',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'de_embedding': ['data/*'],
        
    },

    install_requires = ['numpy','pandas','scikit-rf','matplotlib','scipy'],

    url='https://github.com/aplatag/project_de_embedding_rf.git'
)