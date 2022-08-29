import sys
import os.path

# For Google APIs
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# For dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# For encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

# For Command line compatibility
import argparse
parser = argparse.ArgumentParser(description="Gmail Helper")
parser.add_argument("--manual", action="store_true", default=False, help="specifies if the script is running in manual mode")
parser.add_argument("-o", choices={"email","search","none"}, default="none", help="Send Email, Search Email, Do Nothing")
parser.add_argument("-e", action='store', type=str, help="Email address of recipient")
parser.add_argument("-s", action='store', type=str, default="",help="Subject line")
parser.add_argument("-b", action='store', type=str, default="",help="Body of email")
parser.add_argument("-k", action='store', type=str, help="Search keyword")

args = parser.parse_args()
mode = args.manual
action = args.o
recipient = args.e
subject = args.s
body = args.b
keyword = args.k

#print(mode, action, recipient, subject, body, keyword)

# Handling without recipient email sent request, Subject and Body can be handled if necessary
if mode and action == "email" and not recipient:
    print("Error on dependency for manual mode")
    sys.exit(1)
elif mode and action == "email" and recipient:
    # Warning for empty subject line and/or body
    if subject =="" and body == "":
        print("Want to send email without subject and body? [y/N]")
        confirmation = input()
    elif subject =="":
        print("Want to send email without subject? [y/N]")
        confirmation = input()
    elif body == "":
        print("Want to send email without body? [y/N]")
        confirmation = input()
    else:
        confirmation = 'Y'
    if(confirmation == 'n' or confirmation == 'N' ):
        print("Action abort")
        sys.exit(1)
else:
    pass

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']
# Email address which will be used to send emails
EMAIL = "test-user@gmail.com"

class my_gmail:
    def __init__(self):
        self.creds = None
        self.own_email = EMAIL
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('gmail', 'v1', credentials=self.creds)

    def add_attachment(self, message, filename):
        content_type, encoding = guess_mime_type(filename)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(filename, 'rb')
            msg = MIMEText(fp.read().decode(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(filename, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(filename, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(filename, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(filename)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

    def build_message(self, destination, obj, body, attachments=[]):
        if not attachments: # no attachments given
            message = MIMEText(body)
            message['to'] = destination
            message['from'] = self.own_email
            message['subject'] = obj
        else:
            message = MIMEMultipart()
            message['to'] = destination
            message['from'] = our_email
            message['subject'] = obj
            message.attach(MIMEText(body))
            for filename in attachments:
                add_attachment(message, filename)
        return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

    def send_email(self, destination, obj, body, attachments=[]):
        return self.service.users().messages().send(
          userId="me",
          body=self.build_message(destination, obj, body, attachments)
        ).execute()

    def search_emails(self, query):
        result = self.service.users().messages().list(userId='me',q=query).execute()
        msg = [ ]
        if 'messages' in result:
            msg.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = self.service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
            if 'messages' in result:
                msg.extend(result['messages'])
        return msg


if __name__ == '__main__':
    worker = my_gmail()
    if(mode):
        if(action=="email"):
            worker.send_email(recipient, subject, body)
        elif(action=="search"):
            emails_matched = worker.search_emails("to:md.rashedul.amin@gmail.com")
            print(emails_matched)
        else:
            print("No action selected")
    else:
        worker.send_email("md.rashedul.amin@gmail.com", "Test subject", "This is the test body of the email")
        emails_matched = worker.search_emails("to:md.rashedul.amin@gmail.com")
        print(messages)
