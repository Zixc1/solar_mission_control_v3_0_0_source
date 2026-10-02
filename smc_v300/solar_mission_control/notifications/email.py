import os, smtplib
from email.message import EmailMessage

def send_email(subject,body,recipients,attachment=None,dry_run=False):
    if dry_run:return {'dry_run':True,'recipients':recipients}
    host,user,password=os.getenv('SMC_SMTP_HOST'),os.getenv('SMC_SMTP_USER'),os.getenv('SMC_SMTP_PASSWORD')
    if not all((host,user,password)):return {'skipped':'email not configured'}
    msg=EmailMessage();msg['Subject']=subject;msg['From']=user;msg['To']=', '.join(recipients);msg.set_content(body)
    if attachment:
        data=open(attachment,'rb').read();msg.add_attachment(data,maintype='application',subtype='pdf',filename=os.path.basename(attachment))
    with smtplib.SMTP_SSL(host) as s:s.login(user,password);s.send_message(msg)
    return {'sent':True}
