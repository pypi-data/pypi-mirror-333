from setuptools import setup, find_packages

setup(
    name='result-portal-lib',
    version='0.1.8',
    author='Adams Animashaun',
    author_email='animashaunadams@gmail.com',
    description='A library for AWS integration with Django',
    long_description=open('README.md').read() if open('README.md', errors='ignore') else 'A library for AWS integration with Django',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/result-portal-lib',  # Optional
    packages=find_packages(),
    install_requires=[
        'boto3>=1.18.63',
        'django>=3.2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)