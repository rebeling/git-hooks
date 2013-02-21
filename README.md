Git-Hooks
=========

Hooks to use in any Git Repository

Running the following command to add the git-hooks as an submodule to your repositry
    
    git submodule add https://github.com/tspycher/git-hooks.git git-hooks
    ln -s `pwd`/git-hooks/commit-msg `pwd`/.git/hooks/commit-msg
    cp git-hooks/etc/mite.config.example git-hooks/etc/mite.config
    cp git-hooks/etc/hipchat.config.example git-hooks/etc/hipchat.config

Currently supporting:
* Checking if Bug Id has been provided (#1234 or #ABC-1234)
* Getting time from commit message and report it to mite.yo.lk
* Sending Message to HipChat

Mite
----

Time gets parsed in the following formats. Every line reports 2hours and 5 minutes:

    "Lorem ipsum dolor sit amet @2h5m Lorem ipsum dolor sit amet" 
    "Lorem ipsum dolor sit amet @2hours5minuts Lorem ipsum dolor sit amet"
    "Lorem ipsum dolor sit amet @2h5min Lorem ipsum dolor sit amet"
    "Lorem ipsum dolor sit amet @2:5 Lorem ipsum dolor sit amet"
    "Lorem ipsum dolor sit amet @125 Lorem ipsum dolor sit amet"
