#
# InkPulp-Quota
#
# Tested on RHEL 7 using Python 2.7.5
#
VERSION='1.0.2'

import pycurl
import yaml
from io import BytesIO
from os import getlogin
from os import getgroups
from socket import gethostname
from socket import gethostbyname
from time import sleep
from sys import argv
from sys import exit

# Functions from the Internet
# Credit: http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def handle_entityref(self, name):
        self.fed.append('&%s;' % name)
    def get_data(self):
        return ''.join(self.fed)

def html_to_text(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
# End of Functions from the Internet

# Load configuration variables
#config     = yaml.load(file('inkpulp-quota.yml'))
config     = yaml.load(file('/etc/inkpulp-quota.yml'))

# Sleep for a moment (see configuration)
# We do this to prevent people from hammering the server.
sleep(config['sleep_delay'])

# Set some variables
buffer     = BytesIO()
username   = getlogin()
hostname   = gethostname().partition('.')[0]
hostipaddr = gethostbyname(gethostname())

# Arguments?
if len(argv) > 1:
  # Help?
  if argv[1] in ['-?', '-h', '-help', '--help']:
    print('Syntax: This command takes no arguments.')
    exit(0)
  # Version?
  if argv[1] in ['-V', '-v', '-version', '--version']:
    print('Client version: ' + VERSION)
    exit(0)
  # If we get here, assume the argument is a
  # username. Checking other user balances
  # is restricted to users in the admin_group
  if config['admin_group'] in getgroups():
    username = argv[1]

# XML Request Template
xmlreqt  = '<?xml version="1.0"?>'
xmlreqt += '<methodCall>'
xmlreqt +=   '<methodName>client.getUserBalance</methodName>'
xmlreqt +=   '<params>'
xmlreqt +=     '<param><value>USERNAME</value></param>'
xmlreqt +=     '<param><value>HOSTNAME</value></param>'
xmlreqt +=     '<param><value>HOSTIPADDR</value></param>'
xmlreqt +=     '<param><value>USERNAME</value></param>'
xmlreqt +=   '</params>'
xmlreqt += '</methodCall>'

# Replace the placeholders with the proper values
xmlreq = xmlreqt
xmlreq = xmlreq.replace('USERNAME', username)
xmlreq = xmlreq.replace('HOSTNAME', hostname)
xmlreq = xmlreq.replace('HOSTIPADDR', hostipaddr)

# Use Curl to send the request.
c = pycurl.Curl()
c.setopt(c.URL, 'http://' + config['server_address'] + '/rpc/clients/xmlrpc')
c.setopt(c.HTTPHEADER, ['User-Agent: InkPulp-Quota/' + VERSION, 'Content-Type: text/xml'])
c.setopt(c.POST, 1)
c.setopt(c.POSTFIELDS, xmlreq)
c.setopt(c.WRITEFUNCTION, buffer.write)
c.perform()
c.close()

# At this point, the programmer is feeling tired and consequently is getting
# lazy. The code below could probably be done better, but this "works".
body = html_to_text(buffer.getvalue().decode('iso-8859-1'));

# If "units" exists in the output, we have something to show.
# Otherwise, return a bland error.
if 'units' in body:
  print('You (' + username + ') have ' + body.replace('units', ' units') + ' remaining.')
  exit(0)
else:
  print('Error: unable to query remaining print quota.')
  exit(1)

# EOF
