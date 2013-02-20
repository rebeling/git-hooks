# install Hooks
import os,sys

def confirm(prompt_str="Confirm", allow_empty=False, default=False):
  fmt = (prompt_str, 'y', 'n') if default else (prompt_str, 'n', 'y')
  if allow_empty:
    prompt = '%s [%s]|%s: ' % fmt
  else:
    prompt = '%s %s|%s: ' % fmt
 
  while True:
    ans = raw_input(prompt).lower()
 
    if ans == '' and allow_empty:
      return default
    elif ans == 'y':
      return True
    elif ans == 'n':
      return False
    else:
      print 'Please enter y or n.'

path = os.path.dirname(os.path.realpath("%s/../" % __file__))
gitPath = path
gitPathFound = False

for i in range(len(path.split('/'))-1):
    if os.path.exists("%s/.git" % gitPath):
        gitPath = os.path.realpath(gitPath)
        gitPathFound = True
        break
    else:
        gitPath += "/.."

if gitPathFound:
    gitHookPath = "%s/.git/hooks" % gitPath
    if confirm("Would you like to install the hooks into %s ?" % gitHookPath):
        print "Installing..."
        sys.exit(0)
else:
    sys.stderr.write("Sorry, could not find an parent .git directory :-/")
    sys.exit(1)