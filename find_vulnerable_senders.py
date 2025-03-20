import imaplib
import email
from email.header import decode_header
import re
from dotenv import load_dotenv
import os

load_dotenv()

# Access the variables
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
MAILBOX = os.getenv("MAILBOX")
BATCHSIZE = int(os.getenv("BATCHSIZE"))



def extract_h_field(dkim_signature):
    """
    Extracts all values in the h= field of a DKIM signature.
    
    :param dkim_signature: The DKIM-Signature header as a string.
    :return: A list of field names found in the h= field.
    """
    match = re.search(r";\s*h=([^;]+);?", dkim_signature, re.IGNORECASE)
    if match:
        h_values = match.group(1).strip().lower()
        return [field.strip() for field in h_values.split(":")]
    return []


try:
    # Establish connection
    mail = imaplib.IMAP4_SSL(MAILBOX)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")  # Select inbox (you can change this to another folder)
 
    # Fetch email UIDs (get all email IDs)
    status, data = mail.uid("search", None, "ALL")
    email_uids = data[0].split()

    # Reverse the list to get the most recent emails first
    email_uids.reverse()

    print(f"Total emails: {len(email_uids)}")

    count = 0
    # Fetch emails in batches of the specified size
    for i in range(0, len(email_uids), BATCHSIZE):
        batch = email_uids[i:i + BATCHSIZE]

        # Fetch the emails in the batch
        status, messages = mail.uid("fetch", b",".join(batch).decode("utf-8"), "(BODY.PEEK[HEADER.FIELDS (From DKIM-Signature)])")

    
        # Loop through all emails and fetch the emails we ar interested in
        for message in messages:
            count += 1

            if isinstance(message, tuple):
                # Parse email content
                msg = email.message_from_bytes(message[1])
                ## Check if there is a DKIM-Signature header
                if("dkim-signature" in msg):
                    # Loop through each DKIM-Signature
                    signature, encoding = decode_header(msg["Dkim-Signature"])[0]
                    if not encoding:
                        encoding: 'ISO-8859-1'
                        
                    if signature:
                            signature = signature.replace('\n', ' ').replace('\r', '')

                            sender = msg.get("From")
                            dkim_signature_fields = extract_h_field(signature)

                            ## Check if the Subject or To headers are not signed
                            if ('subject' not in dkim_signature_fields):
                                print(f"Email from {sender} | DKIM-Signature: {' '.join(dkim_signature_fields)}")

    mail.logout()

except Exception as e:
    raise e