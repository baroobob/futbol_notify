"""
Classes and functions for retrieving information about upcoming events from the
watchESPN website.  Takes a date and returns the days events.
"""

# import statements
import re
import urllib.request
from datetime import datetime
from pytz import timezone
from dateutil.parser import parse
from bs4 import BeautifulSoup

# Constants
TZOFFSETS = {"EDT": -14400}
WATCHESPN_TIMEZONE = 'US/Eastern'


################################################################################
# Classes                                                                      #
################################################################################

class Node(object):
  """ Class for building trees.  """

  def __init__(self, data):
    """ Node class constructor """
    self.data = data
    self.children = []

  
  def append(self, data):
    """ Add a new child node, and return a handle to it. """
    new_child = Node(data)
    self.children.append(new_child)
    return new_child


  def to_indented_text(self, tz, level=0):
    """ Print the data from this node and all the nodes below it for the
    timezone given by tz. """
    indented_text = ""
    indent = ""
    for i in range(level):
      indent += "  "
    if isinstance(self.data, str):
      indented_text += "\n" + indent + self.data + "\n"
    else:
      try:
        indented_text += indent + self.data.to_string(tz) + "\n"
      except:
        indented_text += indent + "Unable to print data of type:"
        indented_text += str(type(self.data)) + "\n"
    for child in self.children:
      indented_text += child.to_indented_text(tz, level + 1)
    return indented_text


  def print(self):
    print(self.to_indented_text())


class Event(object):
  """ Class for keeping track of sporting events.  """

  def __init__(self, name, time, key):
    """ Event constructor """
    self.name = name
    self.time = time
    self.key = key

  def to_string(self, tz):
    """ Convert an event to a string for the timezone given by tz. """
    leading_zero = re.compile(r"^0")
    event_time = self.time.astimezone(timezone(tz)).strftime("%I:%M %p %Z")
    event_time = re.sub(leading_zero, " ", event_time)
    if "cable" in self.key:
      access = "Cable"
    if "internet" in self.key:
      access = "Internet"
    return event_time + " " + self.name + " " + access

  def print(self, tz):
    """ Print an event's string for the timezone given by tz. """
    print(self.to_string(tz))


################################################################################
# Functions                                                                    #
################################################################################

def get_upcoming_events(date):
  """
  This function retrieves the upcoming events from the watchESPN website for
  the date given.
  """

  # put the date in the format used by watchespn
  espn_date = date.strftime("%Y%m%d")
  
  # go get the list of upcoming events at watchespn
  url = 'http://espn.go.com/watchespn/index/_/startDate/'
  url += espn_date + '/type/upcoming/'
  try:
    page = urllib.request.urlopen(url)
  except:
    return "Unable to open " + url
  
  # parse this spaghetti mess of html
  soup = BeautifulSoup(page)

  # setup a list for finding headers
  header = ["h1", "h2", "h3", "h4", "h5", "h6"]

  # build a tree from the data
  data_tree = Node("watchespn")
  sections = soup.body.find_all('section')
  for section in sections:
    # typically each section is a different sport
    section_name = section.find(header).contents[0]
    section_node = data_tree.append(section_name)
    leagues = section.find_all('div', 'league')
    for league in leagues:
      # some sports are divided into leagues
      events = league.find_all('div', 'event')
      dates = league.find_all('div', 'date')
      times = league.find_all('div', 'time')
      keys = league.find_all('div', 'key')
      league_header = league.find(header)
      if league_header:
        # found a name for this league
        league_name = league.find(header).contents[0]
        league_node = section_node.append(league_name)
      for i in range(len(events)):
        event_name = events[i].contents[0].lstrip()
        event_time = parse(dates[i].text + " " + times[i].text, 
          tzinfos=TZOFFSETS)
        event_key = keys[i].text
        event = Event(event_name, event_time, event_key)
        if league_header:
          # this event is associated with a league
          league_node.append(event)
        else:
          # this event is not associated with a league
          section_node.append(event)

  return data_tree
    

if __name__ == "__main__":
  todays_date = datetime.now(timezone(WATCHESPN_TIMEZONE))
  event_data = get_upcoming_events(todays_date)
  event_data.print(USER_TIMEZONE)



