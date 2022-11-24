import time

import mailActions
import threading as th
import messageParsing


def key_capture_thread():
    global keep_going
    input()
    keep_going = False

def getCredentials():
    with open("credentials") as file: creds = file.read().splitlines()
    credentials = {
        "username": creds[0],
        "password": creds[1],
        "imap": 'imap.gmail.com',
        "smtp": "smtp.gmail.com"
    }
    return credentials


if __name__ == "__main__":
    keep_going = True
    th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()


    def checkmailLoop(credentials):
        progress = 0
        imapConnection = mailActions.open_connection(credentials)
        while keep_going:
            try:
                progressBar = ("/", "\\")
                messages = mailActions.getMail(imapConnection)

                for activeEmail in messages:
                    to = activeEmail["From"]
                    newMail = messageParsing.parse(activeEmail["Body"])
                    mailActions.sendMail(credentials, to, newMail.subject, newMail.body)
                    print("Mail Found, Processing")

                print("Checking Mail " + progressBar[progress])
                if progress < 1:
                    progress += 1
                else:
                    progress = 0
                time.sleep(10)
            except:
                continue


    checkmailLoop(getCredentials())
