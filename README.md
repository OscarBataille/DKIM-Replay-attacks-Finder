# Partial-DKIM replay attacks detector

Detect email senders that do not correctly sign the "Subject" header in the DKIM-Signature header. These senders are vulnerable to DKIM-replay attacks with a crafted Subject (especially if they do not sign the "To" header neither).

This tool will connect to an IMAP server and check all the DKIM-Signature headers. If the DKIM-Signature does not include the "Subject" header, then it will be printed on the screen.

# Setup
## Requirements
- Python 3 with the required modules

- Define the configuration in the `.env` file. 
> EMAIL = "example@example.org"
> PASSWORD = "XXXXXXXX"
> MAILBOX = "imap.gmail.com"
> BATCHSIZE = 200

## Usage
```bash
python3 find_vulnerable_senders.py
```
<img width="682" alt="Screenshot 2025-03-20 124757" src="https://github.com/user-attachments/assets/b8b17173-66a4-43cd-a50c-7f3a5c91c27d" />



