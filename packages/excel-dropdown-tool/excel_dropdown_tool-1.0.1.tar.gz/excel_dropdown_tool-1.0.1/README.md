# Excel Dropdown Tool

  

A Python package for automating dropdown creation in Excel files while preserving formatting and formulas.

  

  

## Features

  

- 🚀 Batch process multiple Excel files

- 📊 Maintain original formatting and merged cells

- ⚙️ Dynamic dropdown creation from configuration sheets

- ✅ Microsoft Excel compatibility guaranteed

- 📁 CLI interface for easy automation

  

## Requirements

  

- Python 3.6+

- Microsoft Excel (for proper dropdown visualization)

- Packages:

-  `openpyxl>=3.0.0`

-  `xlsxwriter>=3.0.0`

  

## Installation

  

### From PyPI

  

```bash

pip  install  excel-dropdown-tool
```

  

Note:  Processed  files  work  best  in  Microsoft  Excel.  Other  spreadsheet  applications (e.g., LibreOffice,  Google  Sheets) may not display dropdowns correctly.

  

### Usage

Command-Line  Interface (CLI)

Process  all  Excel  files  in  a  folder:

```bash

excel-dropdown  --input-folder path/to/your/excel/files
```
  
  

### Command Options

```bash

$  excel-dropdown  --help

usage:  excel-dropdown [-h] --input-folder INPUT_FOLDER
Process  Excel  files  with  dropdown  validations

options:

-h,  --help  show  this  help  message  and  exit

--input-folder  INPUT_FOLDER

Path  to  folder  containing  Excel  files  to  process
```
  

### Output Structure

Processed  files  are  saved  in
```
your-input-folder/
	└──  processed_files/
	├──  processed_file1.xlsx
	└──  processed_file2.xlsx
```

## License

**MIT License**  
Copyright (c) 2025 Romin Rajesh Katre

For full license terms, see  [LICENSE](https://license/).