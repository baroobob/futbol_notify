""" Classes for sending email.  """

import smtplib
from email.mime.text import MIMEText
import sys


class smtpServer(object):
  """ Class for sending e-mail from an SMTP server.  """

  def __init__(self, server, userName, passwordFile):
    """ Constructor for SMTP server.  """
    self._server = server
    self._userName = userName
    self._passwordFile = passwordFile


  def send_mail(self, fromAddress, toAddress, subject, message):
    """ Method for sending e-mail from an SMTP server.  """
    # Create a text/plain message from the message text.
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = fromAddress
    msg['To'] = toAddress
    # Replace UTF-8 characters that the terminal can't handle
    asciiSubject = subject.encode(sys.stdout.encoding, 'replace')
    asciiSubject = asciiSubject.decode('utf-8')
      
    try:
      # read e-mail server password from file
      fh = open(self._passwordFile, 'r')
      pw = fh.read()
      fh.close()
    except:
      return "Unable to read password file!"

    try:
      # send e-mail
      server = smtplib.SMTP(self._server)
      server.ehlo()
      server.starttls()
      server.login(self._userName, pw)
      server.sendmail(fromAddress, toAddress, msg.as_string())
      server.quit()
      return "Emailed " + toAddress + " about " + asciiSubject + "."
    except:
      return "Unable to send e-mail!"

