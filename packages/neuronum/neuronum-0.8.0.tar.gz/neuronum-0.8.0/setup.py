from setuptools import setup, find_packages

setup(
    name='neuronum',
    version='0.8.0',
    author='Neuronum Cybernetics',
    author_email='welcome@neuronum.net',
    description='A high-level coding library to build & automate economic data streams - The Neuronum Team',
    packages=find_packages(),
    install_requires=[
        'requests',  
    ],
    python_requires='>=3.6', 
)
