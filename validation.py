import pdfplumber
from datetime import datetime
import pandas as pd
import os

def is_valid_date(date_str, format):
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def extract_passbook_data_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        passbook_data = ""
        # Extract text from each page
        for page in pdf.pages:
            passbook_data += page.extract_text()
    #print(passbook_data)
    return passbook_data


def parse_passbook_data(data):
    passbook_entries = []
    lines = data.split('\n')

    for line in lines:
        # Split the line by whitespace
        parts = line.split()

        # Check if the line has the expected number of parts
        if len(parts) >= 2:
            # Extract values from the parts
            wage_month = parts[0]
            date = parts[1]

            # Validate Wage_Month and Date
            if is_valid_date(date, "%d-%m-%Y") and is_valid_date(wage_month, "%b-%Y"):
                transaction_type = parts[2]
                particulars = " ".join(parts[3:-5])
                epf = int(parts[-5].replace(',', '') if parts[-5].replace(',', '').isdigit() else 0)
                eps = int(parts[-4].replace(',', '') if parts[-4].replace(',', '').isdigit() else 0)
                employee = int(parts[-3].replace(',', '') if parts[-3].replace(',', '').isdigit() else 0)  # Employee Contribution
                employer = int(parts[-2].replace(',', '') if parts[-2].replace(',', '').isdigit() else 0)  # Employer Contribution
                pension = int(parts[-1].replace(',', '') if parts[-1].replace(',', '').isdigit() else 0)  # Pension Contribution
                # Append the extracted values to the list
                passbook_entries.append({
                    "Wage_Month": wage_month,
                    "Date": date,
                    "Transaction_Type": transaction_type,
                    "Particulars": particulars,
                    "EPF": epf,
                    "EPS": eps,
                    "Employee_Contribution": employee,
                    "Employer_Contribution": employer,
                    "Pension": pension
                })
        # Convert passbook_entries to a DataFrame
        #df = pd.DataFrame(passbook_entries)

        # Save DataFrame to Excel file
        #df.to_excel("passbook_data.xlsx", index=False)

    return passbook_entries


def process_pdf_folders(root_directory):
    all_data = {}
    for folder_name in os.listdir(root_directory):
        print(f"processing {folder_name}")
        folder_path = os.path.join(root_directory, folder_name)
        if os.path.isdir(folder_path):
            folder_data = []
            for filename in os.listdir(folder_path):
                if filename.endswith(".pdf"):
                    print(f"processing {filename}")
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
    writer.close()

# Usage example:
root_directory = '/home/dell/Downloads/PFData'
process_pdf_folders(root_directory)


