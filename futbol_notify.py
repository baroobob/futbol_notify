from datetime import datetime, timedelta
from dateutil.parser import parse
from pytz import timezone
import urllib.request
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
import sys

"""
Thinking I should go object-oriented with this to make it more readable.  
The objects are users and information sources. Users have interests, like sports
and teams, e-mail addresses, time zones, 

and information sources have URLs, 

"""
DEBUG = False
if len(sys.argv) > 1 and sys.argv[1] == 'debug':
  DEBUG = True

# takes a datetime object and sleeps until tomorrow at 12 am
def sleep_until_tomorrow(now):
  tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0)
  if DEBUG:
    print(now)
    print(tomorrow)
  nap_duration = tomorrow - now
  print("Napping for " + timedelta_to_string(nap_duration) + ".")
  time.sleep(nap_duration.total_seconds())    


# converts a timedelta object to a human friendly string
def timedelta_to_string(td):
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
    

TZOFFSETS = {"EDT": -14400}
zone = 'US/Eastern'
desired_notice = timedelta(hours=1)

while True:

  # put today's date in the format used by watchespn
  todays_date = datetime.now(timezone(zone)).strftime("%Y%m%d")
  current_datetime = datetime.now(timezone(zone))
  print()
  print(current_datetime)
  
  # go get today's list of upcoming events at watchespn
  url = 'http://espn.go.com/watchespn/index/_/startDate/'
  url += todays_date + '/type/upcoming/'
  page = urllib.request.urlopen(url)
  
  # parse this spaghetti mess of html
  soup = BeautifulSoup(page)
  #print(soup.prettify())
  #exit()
  
  # find the Futbol section
  section = soup.body.find_next('section')
  while section and 'Soccer-Futbol' not in section.text:
    section = section.find_next('section')
  
  if section:
    # find the Futbol leagues
    leagues = section.find_all('div', 'league')
    times_until_start = []
    for league in leagues:
      #if league.find('h3'):
        #message += league.h3.contents[0] + "\n"
      # find the Futbol matches
      events = league.find_all('div', 'event')
      dates = league.find_all('div', 'date')
      times = league.find_all('div', 'time')
      keys = league.find_all('div', 'key')
      message = ""
      for i in range(len(events)):
        event_name = events[i].contents[0].lstrip()
        if "internet" in keys[i].text:
          # if it's available to internet customers that don't have cable
          event_datetime = parse(dates[i].text + " " + times[i].text, 
            tzinfos=TZOFFSETS)
          time_until_start = (event_datetime - current_datetime)
          if time_until_start <= desired_notice:
            # if it starts in less than an hour send an email notice
            event_name = events[i].contents[0].lstrip()
            message += dates[i].text + "\t" + times[i].text + "\t"
            message += event_name + "\n"
            message += "\n"
    
            # Create a text/plain message
            msg = MIMEText(message)
            from_address = 'jimbos.notifications@gmail.com'
            to_address = 'jwbwater@gmail.com'
            msg['Subject'] = event_name
            msg['From'] = from_address
            msg['To'] = to_address
            ascii_event_name = event_name.encode(sys.stdout.encoding, 'replace')
            ascii_event_name = ascii_event_name.decode('utf-8')
            print("Emailing " + to_address + " about " + ascii_event_name)
      
            # send notification e-mail to user
            if not DEBUG:
              try:
                # read e-mail server password from file
                fh = open('gmailpw', 'r')
                pw = fh.read()
                fh.close()
              except:
                print "Unable to read password file!"
              try:
                # gmail smtp server
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login('jimbos.notifications', pw)
                server.sendmail(from_address, to_address, msg.as_string())
                server.quit()
              except:
                # try again?
  
          else:
            # if it starts in more than an hour add time until start to list
            times_until_start.append(time_until_start)
    
    if times_until_start:
      # there are upcoming events today, sleep until time for notification
      nap_duration = min(times_until_start) - desired_notice
      print("There is an upcoming event later today!")
      print("Napping for " + timedelta_to_string(nap_duration) + ".")
      time.sleep(nap_duration.total_seconds())    
    else:
      # there are no more upcoming events today, sleep until tomorrow
      print("There are no more unlocked upcoming events for the remainder of today.")
      sleep_until_tomorrow(current_datetime)

  else:
    # there is no Futbol section, sleep until tomorrow
    print("There is no futbol section right now.")
    sleep_until_tomorrow(current_datetime)






