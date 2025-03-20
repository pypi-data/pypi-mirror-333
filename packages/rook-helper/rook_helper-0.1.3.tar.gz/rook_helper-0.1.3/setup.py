from setuptools import setup, find_packages

setup(
    name='rook_helper',
    packages=find_packages(where='rook_helper'),
    package_dir={'': 'rook_helper'},
    version='0.1.3',
    license='MIT',
    description='Helper',
    author='Tomas Rosas',
    author_email='tomas.rosas@tryrook.io',
    url='https://bitbucket.org/rook-workspace/rook_helpers/src',
    download_url='https://bitbucket.org/rook-workspace/rook_helpers/src/develop',
    keywords=['Rook', 'helper'],
    install_requires=[],
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.11'
    ]
    )
