# Partial-DKIM replay attacks detector
Detect email senders that do not correctly sign the "Subject" header in the DKIM-Signature header. DKIM-Signed emails are vulnerable to DKIM-replay attacks with a crafted Subject.

This tool connects to your IMAP (mail) server and checks the DKIM-Signature headers of the emails. 

# Technical details
An email server can sign outgoing emails with DKIM to prove their authenticity.  The process to sign an email (and verify its authenticity) is described in [RFC 6376](https://datatracker.ietf.org/doc/html/rfc6376)

In the following email header:

`DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=domain.com; s=sim; x=1743065658;h=from:to:subject:date:reply-to:message-id:list-unsubscribe: list-unsubscribe-post:feedback-id:list-id:mime-version: content-type; bh=AtU4LO8mVEwbeltrwKVYqaF0T2u31gb+luFS/Ses0kE=; b=wI+cDGLjRP6X/JKE9nIwoWnRl6xIMsUBVGkEHYPyuzoOeUg+x8m27UlZw5NjdR tWKKzgi9uPa2ZGEQVWR9QXER8FKdOwT2dsTxiNnsOelLK/ERPPFEuWbpLPKObB9I ojQB9gDZ1ZgzdDsQuku5a+uzYc1ZQrQF1bG+7daa6aQAY=`

We can see that the following headers are correctly signed:

`h=from:to:subject:date:reply-to:message-id:list-unsubscribe: list-unsubscribe-post:feedback-id:list-id:mime-version: content-type;`

So what would happen if the outgoing email server did not sign the Subject header (and the To headers)?
In that case, an attacker in possession of a DKIM-signed email from the sender could resend the email to any target address with a crafted subject.

## Example
A legit email is sent from support@legitaddress.com to attacker@attacker.com. It is DKIM-Signed.

```
Content-Type: text/plain; charset=ISO-8859-15
Subject: This is a totally legit email
From: support@legitaddress.com
Mime-Version: 1.0
To: attacker@attacker.com
Content-Transfer-Encoding: 8bit
Date: Wed, 19 Mar 2025 11:51:49 +0100 (CET)
DKIM-Signature: a=rsa-sha256; bh=Nr+g5qu50D67ieoTm8keT66h2fS0yHT+PyAN2T8nQwo=;
 c=relaxed/relaxed; d=legitaddress.com; h=From; s=default; t=1742381509; v=1;
 b=VyWCIdBYM6pnnc/MlL2naFFHViUrmkw7kJckwOAr5S10tLhAuAsdss0jgKrovptqRX3dBc9w
 TQ1TWzCH2E+nmvCPDLpGoYWK1lVMpPv+Iuf2VvU/xoR790dE8GqcAO9id7cFrGb+I6ET6tUf9fb
 xYm5SIQLVI4201KWKKzDiEl0=

Hello this is is a legit email. 
```

In this email, **only the From header is signed**: `h=From;`. The attacker (attacker.com) can send the following email to target@targetdomain.com (notice that **Subject and To** headers were changed). 

Email sent from attacker@attacker.com to target@targetdomain.com
```
Content-Type: text/plain; charset=ISO-8859-15
Subject: **Please connect to http://fakebank.com**
From: support@legitaddress.com
Mime-Version: 1.0
To: **target@targetdomain.com**
Content-Transfer-Encoding: 8bit
Date: Wed, 19 Mar 2025 11:51:49 +0100 (CET)
DKIM-Signature: a=rsa-sha256; bh=Nr+g5qu50D67ieoTm8keT66h2fS0yHT+PyAN2T8nQwo=;
 c=relaxed/relaxed; d=legitaddress.com; h=From; s=default; t=1742381509; v=1;
 b=VyWCIdBYM6pnnc/MlL2naFFHViUrmkw7kJckwOAr5S10tLhAuAsdss0jgKrovptqRX3dBc9w
 TQ1TWzCH2E+nmvCPDLpGoYWK1lVMpPv+Iuf2VvU/xoR790dE8GqcAO9id7cFrGb+I6ET6tUf9fb
 xYm5SIQLVI4201KWKKzDiEl0=

Hello this is is a legit email. 
```

**This email will correctly pass the DKIM (and therefore DMARC) checks on targetdomain.com, even if it has been tampered with.** 

# Real-life exploitation
If the `Content-Type` header is not signed, you can hide the original signed body entirely with
`Content-Disposition: attachment;filename=ticket.jpg`.

![image](https://github.com/user-attachments/assets/7e306e26-d089-43a4-a255-5c7928a88ba7)

Note: There is often a timestamp `t=` tag in the DKIM-Signature. Many web servers would not accept an email that was signed too long ago. 

# Setup
## Requirements
- Python 3 with the required modules

- Define the configuration in the `.env` file.
  
```
EMAIL = "example@example.org"
PASSWORD = "XXXXXXXX"
MAILBOX = "imap.gmail.com"
BATCHSIZE = 200
```

## Usage
```bash
python3 find_vulnerable_senders.py
```
<img width="682" alt="Screenshot 2025-03-20 124757" src="https://github.com/user-attachments/assets/b8b17173-66a4-43cd-a50c-7f3a5c91c27d" />



