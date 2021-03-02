import urllib.request
import sys

URL = sys.argv[1]
request = urllib.request.urlopen(URL)

resp = str(request.read())
print(resp)