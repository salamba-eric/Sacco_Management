import numpy
import gspread
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

scope = [
"https://www.googleapis.com/auth/drive", \
"https://www.googleapis.com/auth/drive.file", \
"https://www.googleapis.com/auth/drive.readonly", \
"https://www.googleapis.com/auth/spreadsheets", \
"https://www.googleapis.com/auth/spreadsheets.readonly"	]

# Notes
"""
	The print statements are not necessary and serve to show the progress of the function.
	Various errors may be encountered when network connectivity is unstable. Ensure it's stable. TransportError, ConnectionError are some of the errors
	The numpy package is due to it's efficiency as compared to python lists. Feel free to change it
	The spreadsheet_id will still need to be changed to the relevant one.
	'update_cell', line 35 for me should be retained as True or removed to change a single line
	'Value', line 36 for me needs to be changed to 'Status' or whatever you need to change.
"""

def Update(customer_file = "text/selected_applicant_details.txt", identifier_keys = ("OFFICIAL NAME", "Timestamp","GOVERNMENT ID NUMBER") , update_cell = True, update_time = True):
    # The lines in download database that setup the google sheets we're working on
    spreadsheet_id = "14gCKW6p4FY3Ni57QkknUBtGmTVNkX9tWjxCzQpCfZJ0"
    creds = ServiceAccountCredentials.from_json_keyfile_name("token/token.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id)
    worksheet = sheet.get_worksheet(0)
    data = numpy.array(worksheet.get_all_values())


    # Now we update the sheets
    update_cell = True
    value = 'STATUS'
    # Dynamic assignment of columns. This version is never out of date
    keys = data[0] 
    values = range(len(keys))
    user_details = dict(zip(keys, values))
    # --- Parse the customer info
    def customer__identifier(file):
        customer_details_file = open(file, 'r')
        file_data =  list( customer_details_file.readlines() )
        customer_details_file.close()

        # Assuming it takes the format
        # Timestamp\n Name\n Age\n Sex\n ...
        customer_details = [n[:-1] for n in file_data]
        identifiers = []
        for key in identifier_keys:
            identifiers.append(customer_details[user_details[key]])
        
        if update_cell:
            new_value = customer_details[user_details[value]]
        else:
            new_value = customer_details

        return identifiers, new_value

    # --- Find where we need to update
    identifiers, new_value = customer__identifier(customer_file)  # The unique value to use to find the customer. The new value we update to 
    # --- --- The column we're searc hing
    column = data[:, [ user_details[key] for key in identifier_keys ] ]
    customer_row, row = 0, -1
    for m in column:
        row += 1
        truth_value = 0
        for compare_index in range(len(identifier_keys)):
            if identifiers[compare_index] == m[compare_index]:
                truth_value += 1
        if truth_value == 3 :
            customer_row = row
    if customer_row == 0: # Given row 0 contains the column titles, Index cannot remain 0 if the unique identifier exists
        msg = f"Customer not found.\nAssertain that the key -{identifier_keys}- spot in the file containing the customer details.\nAlso confirm that the customer is indeed an applicant."
        raise ValueError(msg)

    if update_cell:
        # --- --- Construct the cell id, then update the file
        cell_number = chr(65 + user_details[value]) + str(customer_row + 1) # Add one because google sheets rows start from 1
        worksheet.update(cell_number, new_value)
        if update_time:
            import datetime
            date = datetime.date.today().strftime("%d/%m/%y")
            time = datetime.datetime.now().strftime("%H:%M:%S")
            time_of_update = f"{date} {time}"
            time_stamp_cell = chr(65 + user_details['TIME OF UPDATE']) + str(customer_row + 1)
            worksheet.update(time_stamp_cell, time_of_update)

    else: # Untested. Doesn't work with empty strings, Invalid date formats
        identifier, new_row = customer__identifier(customer_file)
        worksheet.update(str(customer_row + 1), new_row)




    # --------- Code to verify update. Not to be included in the final draft ---------
    if update_cell:
        update_type = 'Cell '
    else:
        update_type = "Row "
    print(update_type + "... Waiting for server to update")
    print("Update Complete")
    # print()
    # import time
    # time.sleep(2)
    # # Check for a successful update
    # spreadsheet_id = spreadsheet_id
    # creds = ServiceAccountCredentials.from_json_keyfile_name(r"token.json", scope)
    # client = gspread.authorize(creds)
    # sheet = client.open_by_key(spreadsheet_id)
    # worksheet = sheet.get_worksheet(0)
    # print( numpy.array( worksheet.get_all_values() ) )


Update()


