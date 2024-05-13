from utils.file_utils import process_pdf_interest,process_pdf_contribution
from utils.date_utils import months_between_dates

# Usage example:
#root_directory = '/home/dell/Downloads/PFData'
#process_pdf_interest(root_directory)
#process_pdf_contribution(root_directory)
#print(parse_interest_data(extract_passbook_data_from_pdf('KRKCH15913820000010004_2017.pdf')))

# Example usage
date1 = "Mar-2017"
date2 = "Mar-2024"
months = months_between_dates(date1, date2)
print("Number of months between", date1, "and", date2, ":", months)




