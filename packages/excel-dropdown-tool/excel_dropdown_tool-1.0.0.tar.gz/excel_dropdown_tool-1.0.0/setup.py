from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
long_description = (Path(__file__).parent / "README.md").read_text(encoding='utf-8')

# Read requirements from requirements.txt
def parse_requirements(file_path):
    with open(file_path) as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]
    return requirements

setup(
    name='excel-dropdown-tool',
    version='1.0.0',
    author='Romin Katre',
    author_email='romin.katre32.rk@gmail.com',
    description='Excel file processor with dynamic dropdown creation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/romin23/automate-excel-data-validation',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'excel-dropdown=excel_dropdown.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.6',
    license='MIT',
    keywords='excel dropdown automation openpyxl xlsxwriter',
)