# buildoutable-wekan
Wekan board "buildoutisé"
Fast Howto :

    git clone https://github.com/paulla/buildoutable-wekan.git
    cd ./buildoutable-wekan
    wget https://bootstrap.pypa.io/bootstrap-buildout.py
    python bootstrap-buildout.py
    ./bin/buildout -Nv

Edit buildout.cfg (port / bind_ip etc...) as you whish.
Start with :
    ./bin/supervisord
Check with :
    ./bin/supervisorctl
