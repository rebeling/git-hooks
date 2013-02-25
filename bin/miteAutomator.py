import re
import urllib2
import json
import sys, os
import ConfigParser
import argparse
import select


class Mite(object):
    _apiKey = None
    _baseUrl = None
    
    def __init__(self, apiKey, baseUrl):
        self._apiKey = apiKey
        self._baseUrl = baseUrl

    def getUserId(self, name):
        x = self.__request('/users.json?name=%s' % name, supressError = True)
        try:
            return x[0]['user']['id']
        except:
            return None
                
    def getProjectId(self, name):
        x = self.__request('/projects.json?name=%s' % name, supressError = True)
        try:
            return x[0]['project']['id']
        except:
            return None
    
    def getServiceId(self, name):
        x = self.__request('/services.json?name=%s' % name, supressError = True)
        try:
            return x[0]['service']['id']
        except:
            return None
    
    def addTime(self,note, project=None, service=None):
        if project: projectId = self.getProjectId(project)
        else: projectId = 0
        if service: serviceId = self.getServiceId(service)
        else: serviceId = 0

        try:
            timestring = re.search("(?<=\\@).*?(?=\\s)", note).group()
        except:
            sys.stderr.write("No timestring provided in commit message\n")
            return True
            
        note = note.replace("@%s" % timestring, "")
        minutes = 0
        if ":" in timestring:
            x = "".join(re.findall("\d|:+", timestring)).split(":")
            minutes = (int(x[0]) * 60) + int(x[1])
        elif "m" in timestring or "h" in timestring:
            timestring = "".join(re.findall("\d|h|m+", timestring))
            minutes = (int(re.search("\d*(?=h)", timestring).group()) * 60) + int(re.search("\d*(?=m)", timestring).group())
        else:
            minutes = int("".join(re.findall("\d+", timestring)))

        if not minutes:
            sys.stderr.write("Could not get minutes\n")
            return True
            
        data = {"time-entry":{"minutes":minutes,
            "note":note,
            "service_id":serviceId,
            "project_id":projectId,
            #"user-id":1234
        }}
        x = self.__request('/time_entries.json', json.dumps(data))
        
        if x:
            project = x['time_entry']['project_name'] if 'project_name' in x['time_entry'] else None
            print "Added %i minutes for project %s" % (x['time_entry']['minutes'],project)
            return True
        return False
        
    def __request(self, url, body = None, supressError = False):
        response = None
        request = urllib2.Request(self._baseUrl+url)

        # Header Stuff
        request.add_header("Content-Type", "application/json")
        request.add_header('X-MiteApiKey', self._apiKey)

        if body: request.add_data(body)
        
        # perform the request
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as (code):
            if not supressError:
                sys.stderr.write("Got Error %s - %s\n" % (str(code), self._baseUrl+url))
            return False
        
        if response:
            return json.loads(str(response.read()))
        else:
            return True

if __name__ == '__main__':
    # echo "This a text @1h20m with time in it" | python miteAutomator.py -c mite.config 
    parser = argparse.ArgumentParser(description='Adds Time Information to mite')
    parser.add_argument('--config', '-c', dest='configfile', action='store', default="mite.config", help='Configfile for Mite')
    args = parser.parse_args()

    try:
        c = ConfigParser.RawConfigParser()
        c.read(args.configfile)
    except:
        sys.stdout.write("There is no configfile (%s) ignoring this hook...\n" % args.configfile)
        sys.exit(0)
    
    if select.select([sys.stdin,],[],[],0.0)[0]:
        timestring = sys.stdin.read()
    else:
        sys.stderr.write("No commit Message Provided\n")
        sys.exit(1)
        
    section = "mite"
    apikey = c.get(section, "apikey") if c.has_section(section) and c.has_option(section, "apikey") else None
    baseuri = c.get(section, "baseuri") if c.has_section(section) and c.has_option(section, "baseuri") else None
    project = c.get(section, "project") if c.has_section(section) and c.has_option(section, "project") else None
    service = c.get(section, "service") if c.has_section(section) and c.has_option(section, "service") else None
    
    if not apikey or not baseuri:
        sys.stderr.write("Could not get Apikey and/or baseuri from configfile\n")
        sys.exit(1)
    
    m = Mite(apiKey=apikey, baseUrl=baseuri)
    if m.addTime(timestring, project=project, service=service):
        sys.exit(0)
    sys.exit(255)
