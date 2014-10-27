""" Classes for sending email.  """

import smtplib
from email.mime.text import MIMEText
import sys


class smtpServer(object):
  """ Class for sending e-mail from an SMTP server.  """

  def __init__(self, server, credentials_file):
    """ Constructor for SMTP server.  """
    self._server = server
    self._credentials_file = credentials_file
    try:
      # read e-mail server credentials from file
      fh = open(self._credentials_file, 'r')
      self._username = fh.readline().replace('\n','')
      self._password = fh.readline().replace('\n','')
      fh.close()
    except:
      return "Unable to read credentials file!"


  def get_username(self):
    """ Method to return username.  """
    return self._username


  def send_mail(self, from_address, to_address, subject, message):
    """ Method for sending e-mail from an SMTP server.  """
    # Create a text/plain message from the message text.
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    # Replace UTF-8 characters that the terminal can't handle
    asciiSubject = subject.encode(sys.stdout.encoding, 'replace')
    asciiSubject = asciiSubject.decode('utf-8')
      
    print(from_address)
    print(to_address)
    print(self._username)
    print(self._password)
    try:
      # send e-mail
      server = smtplib.SMTP(self._server)
      server.ehlo()
      server.starttls()
      server.login(self._username, self._password)
      server.sendmail(from_address, to_address, msg.as_string())
      server.quit()
      return "Emailed " + to_address + " about " + asciiSubject + "."
    except:
      return "Unable to send e-mail!"

