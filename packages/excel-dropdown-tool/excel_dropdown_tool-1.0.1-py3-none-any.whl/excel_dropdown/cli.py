import os
from openpyxl import load_workbook
from openpyxl import Workbook as pywb  
from .utils import copy_sheet, get_dropdown_mappings, apply_dropdowns_xlsxwriter
from tqdm import tqdm
import argparse


def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Process Excel files with dropdown validations')
    parser.add_argument('--input-folder', type=str, required=True,
                      help='Path to folder containing Excel files to process')
    args = parser.parse_args()

    # Create output directory
    input_folder = args.input_folder
    output_folder = os.path.join(input_folder, "processed_files")
    os.makedirs(output_folder, exist_ok=True)

    # Process files
    for filename in tqdm(os.listdir(input_folder)):
        if not filename.lower().endswith('.xlsx'):
            continue

        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"processed_{filename}")

        try:
            # Step 1: Create template with OpenPyXL
            wb = load_workbook(input_path)
            template_path = os.path.join(input_folder, 'TEMP_TEMPLATE.xlsx')

            new_wb = pywb()
            new_wb.remove(new_wb.active)
            new_ws = copy_sheet(wb['eBB ver2'], new_wb)
            dropdown_mappings = get_dropdown_mappings(wb['Dropdowns'])
            new_wb.save(template_path)

            # Step 2: Create final version with XlsxWriter dropdowns
            apply_dropdowns_xlsxwriter(
                template_path,
                output_path,
                dropdown_mappings
            )

            # Cleanup temporary file
            os.remove(template_path)
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
            continue

if __name__ == "__main__":
    main()