from setuptools import find_packages, setup

setup(
    name='rococo-email-parser',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/EcorRouge/rococo-email-parser',
    license='MIT',
    author='Mikhail Burilov',
    author_email='burilovmv@gmail.com',
    description='A Python library to parse emails',
    entry_points={
        'console_scripts': [
        ],
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pydantic<3.0.0,>=2.1.0',
        'python-dateutil<3.0.0,>=2.1.0',
        'beautifulsoup4==4.12.2',
        'chardet==5.2.0'
    ],
    python_requires=">=3.10"
)
