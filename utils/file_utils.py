import pandas as pd
import os
from parser.passbook_parser import parse_passbook_contribution,extract_passbook_data_from_pdf,parse_interest_data

def list_subdirectories(root_directory):
    subdirectories = []
    for entry in os.listdir(root_directory):
        full_path = os.path.join(root_directory, entry)
        if os.path.isdir(full_path):
            subdirectories.append(entry)
    return subdirectories

def process_contribution(folder_path):
    folder_data = []
    file_names = sorted(os.listdir(folder_path))  # Sort file names alphabetically
    for filename in file_names:
        if filename.endswith(".pdf"):
            passbook_data = extract_passbook_data_from_pdf(os.path.join(folder_path, filename))
            parsed_data = parse_passbook_contribution(passbook_data)
            folder_data.extend(parsed_data)
    return folder_data

def process_pdf_contribution(root_directory):
    all_data = {}
    subdirectories = list_subdirectories(root_directory)
    for folder_name in subdirectories:
        folder_path = os.path.join(root_directory, folder_name)
        print(f"Processing folder: {folder_path}")
        folder_data = process_contribution(folder_path)
        all_data[folder_name] = folder_data
    output_file = "passbook_contribution_combined.xlsx"
    write_data_to_excel(output_file,all_data)

def process_interest(folder_path):
    folder_data = []
    file_names = sorted(os.listdir(folder_path))  # Sort file names alphabetically
    for filename in file_names:
        if filename.endswith(".pdf"):
            print(f"processing {filename}")
            passbook_data = extract_passbook_data_from_pdf(os.path.join(folder_path, filename))
            parsed_data = parse_interest_data(passbook_data)
            print(f"parsing{parsed_data}")
            folder_data.extend(parsed_data)
    return folder_data

def process_pdf_interest(directory):
    all_data = {}
    subdirectories = list_subdirectories(directory)
    for folder_name in subdirectories:
        folder_path = os.path.join(directory, folder_name)
        print(f"Processing folder: {folder_path}")
        folder_data = process_interest(folder_path)
        all_data[folder_name] = folder_data
    output_file = "passbook_interest_combined.xlsx"
    write_data_to_excel(output_file, all_data)

def write_data_to_excel(output_file,all_data):
    print("writing data to file")

    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
    for folder_name, data in all_data.items():
        df = pd.DataFrame(data)
        df.to_excel(writer, index=False, sheet_name=folder_name)
    #writer.save()  # Save the workbook after writing all sheets
    writer.close()