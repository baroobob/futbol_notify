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

# Constants
SMTP_SERVER = 'smtp.gmail.com:587'
USER_NAME = 'jimbos.notifications'
PASSWORD_FILE = 'gmailpw'
FROM_ADDRESS = 'jimbos.notifications@gmail.com'
TO_ADDRESS = 'jwbwater@gmail.com'
USER_TIMEZONE = 'US/Arizona'
WATCHESPN_TIMEZONE = 'US/Eastern'


DEBUG = False
if len(sys.argv) > 1 and sys.argv[1] == 'debug':
  DEBUG = True


################################################################################
# Functions & Procedures                                                       #
################################################################################

def sleep_until_tomorrow():
  """ Sleeps until tomorrow at 12 am EDT. """
  now = datetime.now(timezone(WATCHESPN_TIMEZONE))
  tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0)
  if DEBUG:
    print(now)
    print(tomorrow)
  nap_duration = tomorrow - now
  print("Napping for " + timedelta_to_string(nap_duration) + ".")
  time.sleep(nap_duration.total_seconds())    


def timedelta_to_string(td):
  """ Takes a timedelta object and returns a days, hours, minutes string. """
  num_seconds = td.total_seconds()
  td_string = ""
  days = int(num_seconds / (24*60*60))
  if days > 1:
    # days plural
    td_string += str(days) + " days, "
  elif days > 0:
    # day singular
    td_string += "1 day, "
  hours = int((num_seconds / (60*60)) % 24)
  if hours > 1:
    # hours plural
    td_string += str(hours) + " hours, "
  elif hours > 0:
    # hours singular
    td_string += "1 hour, "
  minutes = int((num_seconds / 60) % 60)
  if int(num_seconds / 60) > minutes:
    # insert an and if there are days or hours
    td_string += "and "
  if minutes > 1:
    # minutes plural
    td_string += str(minutes) + " minutes"
  elif minutes > 0:
    # minutes singular
    td_string += "1 minute"
  if DEBUG:
    print(num_seconds)
    print(days)
    print(hours)
    print(minutes)
  return td_string
    

################################################################################
# Main program                                                                 #
################################################################################

if __name__ == "__main__":

  # setup mail server
  mailServer = smtpServer(SMTP_SERVER, USER_NAME, PASSWORD_FILE) 

  # setup regular expression to strip leading zero from day of the month
  leading_zero = re.compile(r"^0")

  while True:
  
    # print the current date and time for the server log
    print()
    print(datetime.now(timezone(USER_TIMEZONE)))
    
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
      email_result = mailServer.send_mail(FROM_ADDRESS, TO_ADDRESS, subject, message)
      print(email_result)
      if "Emailed" in email_result:
        break
      else:
        # if mail wasn't sent, try again soon
        nap_duration = timedelta(minutes=5)
        print("Napping for " + timedelta_to_string(nap_duration) + ".")
        time.sleep(nap_duration.total_seconds())    
  
    # sleep until tomorrow
    sleep_until_tomorrow()
  
  
  
  
  
  
