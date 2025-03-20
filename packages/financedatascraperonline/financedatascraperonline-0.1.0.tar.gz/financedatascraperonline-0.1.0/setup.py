from setuptools import find_packages, setup

setup(
    name='financedatascraperonline',
    packages=find_packages(include=['financedatascraperonline']),
    version='0.1.0',
    description='Library for scraping financial data from online sources',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Avilasha Jinia Haldar',
    install_requires=['pandas', 'numpy', 'requests', 'lxml', 'yfinance'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'unittest', 'pandas', 'numpy'],
    test_suite='tests',
)