import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
#read the text file
with open('text/selected_applicant_details.txt', 'r') as file:
    Timestamp  = file.readline().strip()
    Official_Name  = file.readline().strip()
    Age  = file.readline().strip()
    Sex  = file.readline().strip()
    Government_ID  = file.readline().strip()
    Government_ID_Photo  = file.readline().strip()
    Occupation  = file.readline().strip()
    PaySlipImage  = file.readline().strip()
    LoanDuration  = file.readline().strip()
    LoanAmount  = file.readline().strip()
    PhoneNo  = file.readline().strip()
    Email  = file.readline().strip()
    ApplicantEssay  = file.readline().strip()
    Status  = file.readline().strip()
    Time_of_Update  = file.readline().strip()

def main():    
    # Gmail SMTP settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Use TLS port 587
    smtp_username = 'mulemr118@gmail.com'
    smtp_password = 'dzsnhhiqfeefqqic'

    # Create the email message
    from_email = 'mulemr118@gmail.com'
    to_emails = [Email]

    denial_message = f"""
    Dear {Official_Name},

    We regret to inform you that your recent loan application has been carefully reviewed, and unfortunately, we are unable to approve it at this time. We understand that this news may be disappointing, and we appreciate your interest in our services.

    If you have any questions or would like more information about the decision, please contact our customer support team. We are here to assist you with any concerns you may have.

    Thank you for considering MOZZLE COMPANY, and we wish you the best in your financial endeavors.

    Sincerely,
    MOZZLE COMPANY.
    +254753783226.
    """

    # Create the email message for denial
    subject_denied = 'Notice of Loan Application Denial'

    msg_denied = MIMEMultipart()
    msg_denied['From'] = from_email
    msg_denied['To'] = ', '.join(to_emails)  # Combine multiple recipients into a single string
    msg_denied['Subject'] = subject_denied

    msg_denied.attach(MIMEText(denial_message, 'plain'))

    # Connect to the Gmail SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Use TLS encryption
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(from_email, to_emails, msg_denied.as_string())
        server.quit()

        print('Rejection Email sent successfully')
    except Exception as e:
        print(f'Rejection Email could not be sent. Error: {str(e)}')

main()

