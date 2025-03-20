from setuptools import setup, find_packages

setup(
    name='AsroNLP',
    version='0.1.7',
    author='Asro',
    author_email='asro@raharja.info',
    description='Sebuah perpustakaan Python untuk prapemrosesan teks, stemming, dan analisis sentimen khusus Bahasa Indonesia.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/asroharun6/AsroNLP',
    packages=find_packages(),  # Secara otomatis menemukan semua paket Python termasuk subpaket
    include_package_data=True,  # Memastikan semua data yang dideklarasikan melalui MANIFEST.in disertakan dalam paket
    package_data={  # Menentukan secara eksplisit direktori paket mana yang mengandung data
        'asro_nlp': [
            'data/*.txt',
            'data/*.xlsx'
        ],
    },
    install_requires=[
        'pandas>=1.0.0,<2.0.0',  # Menjamin kompatibilitas dengan versi tertentu dari pandas
        'nltk>=3.5',             # Memastikan nltk di atau di atas versi 3.5
        'openpyxl>=3.0.0'        # Memastikan openpyxl di atau di atas versi 3.0.0
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
