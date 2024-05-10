import pandas as pd
import os
from parser.passbook_parser import parse_passbook_data,extract_passbook_data_from_pdf

def process_pdf_folders(root_directory):
    all_data = {}
    folder_names = sorted(os.listdir(root_directory))  # Sort folder names alphabetically
    for folder_name in folder_names:
        folder_path = os.path.join(root_directory, folder_name)
        print(f"processing folder{folder_path}")
        if os.path.isdir(folder_path):
            folder_data = []
            file_names = sorted(os.listdir(folder_path))  # Sort file names alphabetically
            print(f"processing file{file_names}")
            for filename in file_names:
                if filename.endswith(".pdf"):
                    passbook_data = extract_passbook_data_from_pdf(os.path.join(folder_path, filename))
                    parsed_data = parse_passbook_data(passbook_data)
                    folder_data.extend(parsed_data)
            all_data[folder_name] = folder_data
    write_data_to_excel(all_data)


def write_data_to_excel(all_data):
    print("writing data to file")
    output_file = "passbook_data_combined.xlsx"
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    for folder_name, data in all_data.items():
        df = pd.DataFrame(data)
        df.to_excel(writer, index=False, sheet_name=folder_name)
    #writer.save()  # Save the workbook after writing all sheets
    writer.close()