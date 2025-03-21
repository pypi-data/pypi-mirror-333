from setuptools import setup, find_packages

setup(
    name='blockchain-utils',
    version='0.1.1',
    description='blockchain utils',
    author='BadDevilZ',
    author_email='mazda266@gmail.com',
    include_package_data=True,
    install_requires=[
        'web3==7.8.0',
        'solders==0.26.0',
        'bech32==1.2.0',
        'base58==2.1.1',
        'blake256==0.1.1',
        'buidl==0.2.36',
        'cbor==1.0.0',
        'monero==1.1.1',
    ],
    python_requires='>=3.8,<4',
    license='EULA',
    zip_safe=False,
    keywords='crypto blockchain',
    packages=find_packages(exclude=['docs', 'tests']),
)
