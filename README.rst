===========
user-config
===========

::

    cd "${HOME}"
    git clone git@github.com:vakaras/user-config.git .user-config
    cd .user-config
    make
    ./waf configure --apps=bash,keyboard,tmux,vim
