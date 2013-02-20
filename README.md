git-hooks
=========

Hooks to use in any Git Repository

Running the following command to add the git-hooks to your repositry
    
    git submodule add https://github.com/tspycher/git-hooks.git git-hooks
    ln -s `pwd`/git-hooks/commit-msg `pwd`/.git/hooks/commit-msg
    cp git-hooks/etc/mite.config.example git-hooks/etc/mite.config
