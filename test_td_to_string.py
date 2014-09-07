""" Tests for the timedelta_to_string function in futbol_notify.py """

from datetime import timedelta
from futbol_notify import timedelta_to_string


# try cases with all combinations of:
# no days
# one day
# multiple days
# no hours
# one hour
# multiple hours
# no minutes
# one minute
# multiple minutes

for d in [0, 1, 2]:
  for h in [0, 1, 2]:
    for m in [0, 1, 2]:
      td = timedelta(days=d, hours=h, minutes=m)
      print(timedelta_to_string(td) + ".")

