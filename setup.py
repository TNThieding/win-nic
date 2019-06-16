import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    install_requires = [
        'enum34',
        'texttable'
        ],

    name             = 'win-nic',
    version          = '2.0.0',
    author           = 'Tyler N. Thieding',
    author_email     = 'python@thieding.com',
    maintainer       = 'Tyler N. Thieding',
    maintainer_email = 'python@thieding.com',
    url              = 'https://github.com/TNThieding/win-nic',
    description      = 'Python package to interface with network intetrface cards (NICs) on Windows-based computers.',
    long_description = long_description,
    download_url     = 'https://github.com/TNThieding/win-nic',
    classifiers      = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: System :: Networking',
        ],
    license          = 'MIT License',
    packages=setuptools.find_packages()
)