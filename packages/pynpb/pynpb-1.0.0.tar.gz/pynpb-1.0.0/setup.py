from setuptools import setup, find_packages

setup(
    python_requires='>=3.7,<3.14',
    name='pynpb',
    version='1.0.0',
    description='Python package to retrieve Nippon Professional Baseball (NPB) data ',
    author='Justin Mende',
    author_email='jkmende05@gmail.com',
    url='https://github.com/jkmende05/pynpb',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests>=2.32.3',
        'pandas>=2.2.3',
        'numpy>=2.2.2',
        'beautifulsoup4>=4.13.3',
    ],
    keywords='baseball sabermetrics data statistics statcast web scraping',
)