import http.client, urllib

class pushoverApp(object):
  """ Class for sending mobile phone push notifications.  """

  def __init__(self, appToken):
    """ Constructor for SMTP server.  """
    self._appToken = appToken

  def send_notification(self, userKey, message):
    """ Method for sending mobile phone push notifications via pushover.  """
    try:
      conn = http.client.HTTPSConnection("api.pushover.net:443")
      conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
          "token": self._appToken,
          "user": userKey,
          "message": message,
        }), { "Content-type": "application/x-www-form-urlencoded" })
      response = conn.getresponse()
      #print(response.status)
      #print(response.reason)
      #print(response.read())
      #print(response.getheaders())
      if response.status == 200:
        return "Pushed notification to " + userKey + "."
      # 4xx HTTP responses from pushover mean this request will fail every time
      elif response.status > 400:
        return "Failed to send notification, do not resend."
      else:
        return "Failed to send notification, try again later."
    except:
      return "Unable to send push notification!"


