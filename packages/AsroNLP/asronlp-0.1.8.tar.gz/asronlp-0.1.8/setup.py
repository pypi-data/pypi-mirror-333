from setuptools import setup, find_packages

setup(
    name='AsroNLP',
    version='0.1.8',
    author='Asro',
    author_email='asro@raharja.info',
    description='A simple NLP tool for processing and analyzing text in the Indonesian language.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/asroharun6/AsroNLP',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'asro_nlp': ['data/*.*'],
    },
    install_requires=[
        'pandas',
        'nltk',
        'openpyxl'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: Indonesian',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
