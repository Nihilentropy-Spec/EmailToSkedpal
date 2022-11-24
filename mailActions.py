import datetime
import email
import imaplib
from smtplib import SMTP_SSL, SMTP_SSL_PORT


def open_connection(credentials):
    connection = imaplib.IMAP4_SSL(credentials["imap"])
    connection.login(credentials["username"], credentials["password"])
    print("Opening Connection")
    return connection


def getMail(openConnection):
    mail = openConnection
    mail.list()
    mail.select('inbox')
    result, data = mail.uid('search', None, "ALL") # (ALL/UNSEEN)
    i = len(data[0].split())

    messagesList = []

    for x in range(i):
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        # Header Details
        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
        subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

        # Get Message Parts and add to Dict
        message = {}
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                message["From"] = email_from
                message["To"] = email_to
                message["Date"] = local_message_date
                message["Subject"] = subject
                message["Body"] = body.decode('utf-8')
            else:
                continue
            messagesList.append(message)
        # Delete Message once finished
        mail.uid('STORE', latest_email_uid, '+FLAGS', '(\\Deleted)')
        mail.expunge()

    return messagesList


def sendMail(credentials, to, subject, body):
    SMTP_HOST = credentials["smtp"]
    SMTP_USER = credentials["username"]
    SMTP_PASS = credentials["password"]
    from_email = credentials["username"]
    to_emails = [to]

    # Build Headers
    headers = f"From: {from_email}\r\n"
    headers += f"To: {', '.join(to_emails)}\r\n"
    headers += f"Subject: {subject}\r\n"

    # Assemble Message
    email_message = headers + "\r\n" + body

    # Connect and Login to SMTP, then send
    smtp_server = SMTP_SSL(SMTP_HOST, port=SMTP_SSL_PORT)
    # smtp_server.set_debuglevel(0)  # SMTP Debug
    smtp_server.login(SMTP_USER, SMTP_PASS)
    smtp_server.sendmail(from_email, to_emails, email_message)

    # Disconnect
    smtp_server.quit()