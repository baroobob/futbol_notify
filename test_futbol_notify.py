""" Tests for the timedelta_to_string function in futbol_notify.py """

from datetime import timedelta
from futbol_notify import *

def test_timedelta_to_string():
  """ try cases with all combinations of none, singular, and plural """
  for d in [0, 1, 2]:
    for h in [0, 1, 2]:
      for m in [0, 1, 2]:
        td = timedelta(days=d, hours=h, minutes=m)
        print(timedelta_to_string(td) + ".")


def test_log():
  """ test log function """
  log("logfile test")


if __name__ == "__main__":
  #test_timedelta_to_string()
  test_log()
