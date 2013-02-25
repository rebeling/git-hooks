import urllib2
import json
import sys, os
import ConfigParser
import argparse
import select

class HipChat(object):
    _token = None
    _baseUri = "https://api.hipchat.com"
    
    def __init__(self, token):
        self._token = token

    def _doIt(self, url, data = None):
        finalUrl = "%s%s?auth_token=%s&format=json" % (self._baseUri, url, self._token)
        request = urllib2.Request(finalUrl)
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        if data: 
            urldata = "&".join( "%s=%s"%item for item in data.items() )
            request.add_data(urldata)

        response = urllib2.urlopen(request)       
        return json.loads(response.read())

    def getRoom(self, name):
        url = "/v1/rooms/list"
        x = self._doIt(url)
        for r in x['rooms']:
            if str(name).lower() in str(r['name']).lower():
                return r
        return None

    def postToRoom(self, room, text, senderName = "John Doe", notify = 0, color = "red"):
        if not 'room_id' in room:
            return False
        
        url = "/v1/rooms/message"
        data = {'room_id':room['room_id'], 'from':senderName, 'message':text, 'notify':notify, 'color':color}
        return self._doIt(url,data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HipChat Message client')
    parser.add_argument('--config', '-c', dest='configfile', action='store', default="hipchat.config", help='Configfile for HipChat')
    args = parser.parse_args()
    
    try:
        c = ConfigParser.RawConfigParser()
        c.read(args.configfile)
    except:
        sys.stdout.write("There is no configfile (%s) ignoring this hook...\n" % args.configfile)
        sys.exit(0)

    if select.select([sys.stdin,],[],[],0.0)[0]:
        message = sys.stdin.read()
    else:
        sys.stderr.write("No commit Message Provided\n")
        sys.exit(1)

    section = "hipchat"
    token = c.get(section, "token") if c.has_section(section) and c.has_option(section, "token") else None
    roomname = c.get(section, "roomname") if c.has_section(section) and c.has_option(section, "roomname") else None
    sendername = c.get(section, "sendername") if c.has_section(section) and c.has_option(section, "sendername") else None

    if not token or not roomname:
        sys.stderr.write("Could not get token and/or room name from configfile\n")
        sys.exit(1)
    
    hp = HipChat(token)
    r = hp.postToRoom(hp.getRoom(roomname), message, notify = 1, senderName = sendername)
    if "status" in r and r['status'] == "sent":
        sys.exit(0)
    sys.stderr.write("Could not post Message to Hipchat")
    sys.exit(1)