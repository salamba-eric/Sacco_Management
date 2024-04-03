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

    pending_message = f"""
    Dear {Official_Name},

    Thank you for submitting your loan application on the {Timestamp} to MOZZLE COMPANY. We have received your request and are currently in the process of reviewing the details.

    Application Status: Pending Review

    Our team is working diligently to assess your application thoroughly. We will notify you of the decision as soon as possible. In the meantime, if you have any questions or need additional information, please feel free to contact our customer support.

    We appreciate your patience and understanding.

    Best Regards,
    MOZZLE COMPANY.
    +254753783226.
    """

    # Create the email message for pending
    subject_pending = 'Your Loan Application is Under Review'

    msg_pending = MIMEMultipart()
    msg_pending['From'] = from_email
    msg_pending['To'] = ', '.join(to_emails)  # Combine multiple recipients into a single string
    msg_pending['Subject'] = subject_pending

    msg_pending.attach(MIMEText(pending_message, 'plain'))

    # Connect to the Gmail SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Use TLS encryption
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(from_email, to_emails, msg_pending.as_string())
        server.quit()

        print('Pending Email sent successfully')
    except Exception as e:
        print(f'Pending Email could not be sent. Error: {str(e)}')

main()