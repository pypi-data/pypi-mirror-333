from setuptools import setup, find_packages

setup(
    name='beiker',
    version='0.0.8',
    author='tarantella110',
    author_email='beiker110@126.com',
    description='developed for electronic archive organization.',
    packages=find_packages(),
    install_requires=[
    'pandas',
    'mysql-connector-python',
    'pillow',
    'python-docx',
    'openpyxl',
    # 'PySide6',
    'PyMuPDF'
],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving',
        'Topic :: Text Processing :: General',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)