# chaos_platform
platform for chaos engineering


# db 
the DB of the chaos platform is currently mongoDB.
the DB folder includes 2 scripts, a python script which is the REST api for the mongoDB, And a bash script which initializes the mongoDB to 
include the basic collections and examples.

# injector
the injector folder currently incudes two scripts, The injector slave script and the injector slave api script.
the injector slave must run on a linux machine on the injector user with the /home/injector base dir

# cli 
the cli is made with the click library and is incharge of changing the fault timing interval and interacting witht the db api.

# random picker 
description of random picker 

# master
description of master
