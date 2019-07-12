import os
import smtplib
from email.mime.text import MIMEText

from astropy.table import Table


def send_mails(filename='astropy-core-maintainers.csv',
               dry_run=True, confirm=True):
    me = os.environ['USER'] + '@head.cfa.harvard.edu'

    maints = Table.read(filename)
    for maint in maints:
        recipient = maint['Email address']
        name = maint['Nickname']
        send_mail(recipient, name, dry_run, me, confirm)


def send_mail(recipient, name, dry_run, me, confirm):
    subject = f'Astropy role questionnaire for maintainers'

    first_name = name.split()[0]
    print(first_name, recipient)
    text = f"""\
Hi {first_name},

The Astropy coordination committee would like to solicit your input
regarding your Astropy team role(s).  As agreed at the coordination
meeting last winter, we are starting a new program to regularly ask each
team member a few questions in order to better understand where we stand as
a project in terms of support for each role.

Please take a moment to fill out the following form:

https://docs.google.com/forms/d/1lkxuJNorU-qIstz7-jAfzvJxzZDWRKHtFP7zXy1T4vA/edit

We greatly appreciate your contributions to the project and your response
to these questions, if possible within 2 weeks. Note that a lack of
response for an extended period of time may lead to your role being
declared vacant.

If you have any questions please email coordinators@astropy.org.

Thank you,
The Astropy coordination committee

"""
    cc = 'taldcroft@cfa.harvard.edu'
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = recipient
    msg['Cc'] = cc

    print(msg.as_string())

    if confirm:
        confirm = input('Confirm [y/N] : ')
        if not confirm.strip() == 'y':
            print('\n**Aborting**\n')
            return

    if not dry_run:
        try:
            s = smtplib.SMTP('localhost')
            s.sendmail(me, [recipient] + [cc], msg.as_string())
            s.quit()
            print(f'Sent mail to {recipient}')
        except Exception as err:
            print('')
            print(f'ERROR: sendmail({me}, {recipient}) failed: {err}')
            print(f'{msg.as_string()}')
            raise
