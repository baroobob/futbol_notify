"""
Script which sends me e-mail notifications about upcoming soccer matches that
are available on ESPN's website.
"""

# import statements
import re
import sys
import time
from datetime import datetime, timedelta
from pytz import timezone
from watch_espn import get_upcoming_events
from send_mail import smtpServer
from push_notification import pushoverApp

# Constants
PUSHOVER_APP_TOKEN = "auUec9JTmPxgppGhEzZ3Tcq2iqfCUN"
SMTP_SERVER = 'smtp.gmail.com:587'
USER_NAME = 'jimbos.notifications'
PASSWORD_FILE = 'gmailpw'
FROM_ADDRESS = 'jimbos.notifications@gmail.com'
WATCHESPN_TIMEZONE = 'US/Eastern'

# User constants, will come from a database for a multiuser model
USER_TIMEZONE = 'America/Phoenix'
USER_EMAIL_ADDRESS = 'jwbwater@gmail.com'
PUSHOVER_USER_KEY = "uHvcDKd7sbqgpdRXdHqfs1KyzTiBpF"

################################################################################
# Functions & Procedures                                                       #
################################################################################

def sleep_until_tomorrow():
  """ Sleeps until tomorrow at 12 am EDT. """
  now = datetime.now(timezone(WATCHESPN_TIMEZONE))
  tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0)
  nap_duration = tomorrow - now
  log("Napping for " + timedelta_to_string(nap_duration) + ".")
  time.sleep(nap_duration.total_seconds())    


def timedelta_to_string(td):
  """ Takes a timedelta object and returns a days, hours, minutes string. """
  num_seconds = td.total_seconds()
  days = int(num_seconds / (24*60*60))
  hours = int((num_seconds / (60*60)) % 24)
  minutes = int((num_seconds / 60) % 60)
  td_phrase = []
  # build list of days, minutes, and hours
  if days > 0:
    td_phrase.append(str(days) + " day")
  if days > 1:
    td_phrase[-1] += "s"
  if hours > 0:
    td_phrase.append(str(hours) + " hour")
  if hours > 1:
    td_phrase[-1] += "s"
  if minutes > 0:
    td_phrase.append(str(minutes) + " minute")
  if minutes > 1:
    td_phrase[-1] += "s"
  # insert and, and commas where necessary
  if len(td_phrase) > 2:
    td_phrase[1:1] = ", "
  if len(td_phrase) > 1:
    td_phrase[-1:-1] = " and "
  # handle the case where days, hours, and minutes are all 0
  if len(td_phrase) == 0:
    td_phrase.append("0 minutes")
  td_string = ""
  for word in td_phrase:
    td_string += word
  return td_string
    

def log(message=""):
  """ Appends messages to log file. """
  # The log file name is made by replacing .py with .log and the log file is
  # placed in the same directory as the python file.
  program_name = re.split(r"/",sys.argv[0])[-1]
  logfile_name = program_name.replace(".py","")
  logfile_name += ".log"
  path_to_logfile = sys.argv[0].replace(program_name, logfile_name)
  # Write message to log file. 
  try:
    logfile = open(path_to_logfile, 'a')
    logfile.write(str(message) + "\n")
    logfile.close()
  except:
    exit("Unable to write to log file: " + path_to_logfile)


################################################################################
# Main program                                                                 #
################################################################################

if __name__ == "__main__":

  # setup mail server
  program_name = re.split(r"/",sys.argv[0])[-1]
  path_to_password_file = sys.argv[0].replace(program_name, PASSWORD_FILE)
  mailServer = smtpServer(SMTP_SERVER, USER_NAME, path_to_password_file)
  notificationServer = pushoverApp(PUSHOVER_APP_TOKEN)

  # setup regular expression to strip leading zero from day of the month
  leading_zero = re.compile(r"^0")

  while True:
  
    # record the current date and time for the server log
    log()
    log(datetime.now(timezone(USER_TIMEZONE)))
    
    # go get today's list of upcoming events at watchespn
    todays_date = datetime.now(timezone(WATCHESPN_TIMEZONE))
    event_data = get_upcoming_events(todays_date)
    
    # find the Futbol section
    for section in event_data.children:
      if 'Soccer-Futbol' in section.data:
        message = section.to_indented_text(USER_TIMEZONE)
      
    # Send e-mail
    while True:
      weekday = todays_date.strftime("%A")
      month = todays_date.strftime("%B")
      date = re.sub(leading_zero, "", todays_date.strftime("%d"))
      subject = "Soccer games for " + weekday + ", " + month + " " + date
      email_result = mailServer.send_mail(FROM_ADDRESS, USER_EMAIL_ADDRESS,
        subject, message)
      log(email_result)
      #notification_result = notificationServer.send_notification(
      #  PUSHOVER_USER_KEY, subject + "\n" + message)
      #log(notification_result)
      if "Emailed" in email_result:
      #if "Pushed" in notification_result:
        break
      else:
        # if mail wasn't sent, try again soon
        nap_duration = timedelta(minutes=5)
        log("Napping for " + timedelta_to_string(nap_duration) + ".")
        time.sleep(nap_duration.total_seconds())    
  
    # sleep until tomorrow
    sleep_until_tomorrow()
  
  
  
  
  
  
