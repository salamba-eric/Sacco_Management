import gspread
from google.oauth2 import service_account
import os
os.chdir(os.path.dirname(os.path.realpath(__file__))) #makes paths relative

# Define the scope and credentials
scope = [
"https://www.googleapis.com/auth/drive", \
"https://www.googleapis.com/auth/drive.file", \
"https://www.googleapis.com/auth/drive.readonly", \
"https://www.googleapis.com/auth/spreadsheets", \
"https://www.googleapis.com/auth/spreadsheets.readonly"	]

def download_database():
    # Open the Google Spreadsheet by its title or URL
    spreadsheet_id = "14gCKW6p4FY3Ni57QkknUBtGmTVNkX9tWjxCzQpCfZJ0"
    creds = service_account.Credentials.from_service_account_file("token/token.json", scopes = scope)
    # Authenticate with the Google Sheets API
    client = gspread.authorize(creds) # Error may mean Json file lacks a specific needed Key/Value pair
    # Open the Google Sheet using its ID
    sheet = client.open_by_key(spreadsheet_id) # Error may mean Either id isn't valid, the credentials aren't right or the scopes don't match up
    # Access a specific worksheet within the Google Sheet 
    worksheet = sheet.get_worksheet(0) #Error may indicate the worksheet doesn't exist
    # Read data from the worksheet
    data =  worksheet.get_all_values() 
    return data

#global data
data = download_database()

# select by column     
def select_by_column(column, value):
    user_details = {'Timestamp':0, 'OFFICIAL NAME':1, 'AGE':2, 'SEX':3,\
        'GOVERNMENT ID NUMBER':4, 'photo':5, 'OCCUPATION':6, 'pay slip':7, 'LOAN DURATION':8,\
            'LOAN AMOUNT':9, 'PHONE NUMBER':10, 'EMAIL':11, 'APPLICATION ESSAY':12, "Status": 13, "Time of update": 14}  
    
    if column in user_details:
        column_index = user_details[column]
        return [row for row in data if row[column_index] == value]
    else:
        print('Column not in User Details')
        return None
    
def get_accepted():
    return select_by_column('Status', 'accepted')

def get_pending():
    return select_by_column('Status', '')

def get_rejected():
    return select_by_column('Status', 'rejected')

accepted_applications = get_accepted()
pending_applications = get_pending()
rejected_applications = get_rejected()

def print_accepted():
    output = str()
    for n in accepted_applications:
        output += "|"
        for i in n:
            output += i + "|"
        output += "\n"
    return output

def print_pending():
    output = str()
    for n in pending_applications:
        output += "|"
        for i in n:
            output += i + "|"
        output += "\n"
    return output

def print_rejected():
    output = str()
    for n in rejected_applications:
        output += "|"
        for i in n:
            output += i + "|"
        output += "\n"
    return output

#paths
acceptedtxt = "text/accepted_applications.txt"
rejectedtxt = "text/rejected_applications.txt"
pendingtxt = "text/pending_applications.txt"

#texts
accepted_people = print_accepted()
pending_people = print_pending()
rejected_people = print_rejected()

#write to path
with open(acceptedtxt, 'w') as file:
    file.write(accepted_people)
with open(rejectedtxt, 'w') as file:
    file.write(rejected_people)
with open(pendingtxt, 'w') as file:
    file.write(pending_people)
