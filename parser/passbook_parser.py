import pdfplumber
from utils.date_utils import is_valid_date
def extract_passbook_data_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        passbook_data = ""
        # Extract text from each page
        for page in pdf.pages:
            passbook_data += page.extract_text()
    # print(passbook_data)
    return passbook_data


def parse_passbook_contribution(data):
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
                employee = int(
                    parts[-3].replace(',', '') if parts[-3].replace(',', '').isdigit() else 0)  # Employee Contribution
                employer = int(
                    parts[-2].replace(',', '') if parts[-2].replace(',', '').isdigit() else 0)  # Employer Contribution
                pension = int(
                    parts[-1].replace(',', '') if parts[-1].replace(',', '').isdigit() else 0)  # Pension Contribution
                # Append the extracted values to the list
                passbook_entries.append({
                    "Wage_Month": wage_month,
                    "Date": date,
                    "Employee_Contribution": employee,
                    "Employer_Contribution": employer,
                    "Pension": pension
                })

    return passbook_entries


def parse_interest_data(data):
    """Parse interest-related data."""
    interest_entries = []
    lines = data.split('\n')

    for line in lines:
        if "Taxable Data for the year" in line:
            break  # Stop parsing if this line is found
        if "Int. Updated upto" in line:
            parts = line.split()
            if len(parts) >= 7:
                # Extract date and contributions
                date = parts[3]  # Assuming the date is always at index 3
                if is_valid_date(date, "%d/%m/%Y"):
                    # Remove commas and convert to integers
                    interest_employee = int(parts[4].replace(',', ''))
                    interest_employer = int(parts[5].replace(',', ''))
                    interest_pension = int(parts[6].replace(',', ''))
                    interest_entries.append({
                        "Date": date,
                        "Interest_Employee_Contribution": interest_employee,
                        "Interest_Employer_Contribution": interest_employer,
                        "Interest_Pension": interest_pension
                    })
    return interest_entries




