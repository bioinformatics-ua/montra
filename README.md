emif-fb
=======

[![Join the chat at https://gitter.im/bioinformatics-ua/emif-fb](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/bioinformatics-ua/emif-fb?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

EMIF Platform - Fingerprint Browser 



#### Install Dependecies in Ubuntu

1.  Install pip package

        sudo apt-get install python-pip


2.  Install virtualenv

        sudo pip install virtualenv


3.  Install curl

        sudo apt-get install curl


4.  Install and Start MongoDB

        sudo apt-get install mongodb

        sudo mkdir /data
        sudo mkdir /data/db

        now you have 2 hypotheses:

            1) change the permissions of data and db folders and run "mongod"

            2)sudo /mongod


5.  Install and Configure Apache-solr
        
        sudo apt-get -y install solr-tomcat

        Go to folder emif-fb-root/conf/solr/ and copy all the files to the solr default core configuration 


6.  Install and Configure PostgreSQL

        1)  sudo apt-get install postgresql

        2)  sudo su postgres
            psql 
                CREATE ROLE user superuser;
                CREATE USER emif_dev;
                GRANT user To emif_dev;
                ALTER ROLE user WITH LOGIN;


7.  Install RabbitMQ

        sudo apt-get install rabbit


8.  Install pil

        sudo apt-get install libpython-dev
        sudo apt-get install build-essential
        pip install -r requirements.txt --allow-all-external --allow-unverified pil


9.  Install celery and memcached

        pip install celery==3.1.0 django-celery==3.1.0 python-memcached==1.48 johnny-cache==1.4


10. Install Python package index
        
        pip install psycopg2
        sudo apt-get install libxml-dev
        pip install lxml
        sudo apt-get install libxml2-dev libxslt1-dev python-dev
        pip install cssselect


11.  Install git

        sudo apt-get install git


12. Checkout of the source code

        https://github.com/bioinformatics-ua/emif-fb.git


13. Create and activate virtual environment

        (path) ...\environments>virtualenv emif
        (path) ...\environments\emif\Scripts>activate.bat (for windows users)
        (path) source ...\environments\emif\Scripts>activate (for unix users)


14. Go to project folder
    
        (emif) C:\...\BioInformatics\emif-fb>   


15. Create '~/pgpass' file and insert:

        localhost:5432:*:emif_dev:emif_dev


16. Change permission mode of pgpass file
    
        chmod 600 /home/user/.pgpass

    
17. Install requirements.txt

        pip install -r requirements.txt --allow-all-external

    NOTE: git must be in environment variables and PIP have to be installed.

18. Create a script file

        copy code from: https://gist.github.com/bastiao/c8d3be799dc7c257f01a and paste in conf/ folder

        run the script

19. Run

        python manage.py syncdb
        python manage.py migrate
        python manage.py loaddata emif\fixtures\emif_questionary_1.yaml
        python manage.py runserver

  
        
18. Run Apache-solr as service


        Go to solr folder and Run
        (path).../apache-solr-4.0.0/example>java -jar start.jar


19. Create a folder to documents population characteristic

        mkdir -p emif/static/files/


20. Open browser and write


        localhost:8000


#### Local settings

    $ cat emif/emif/local_settings.py
    EMAIL_HOST = 'address.mail.com'
    EMAIL_HOST_PASSWORD = 'passwd'
    EMAIL_HOST_USER = 'login'
    EMAIL_PORT = 25
    EMAIL_USE_TLS = True


#### Integration with github issues and releases



    GITHUB_USERNAME='githubusername'
    GITHUB_PASSWD='pass'
    GITHUB_ACCOUNT='bioinformatics-ua'
    GITHUB_REPO='emif-fb'


#### Start the virtual environment and developement(always)

    1) Go to solr folder and Run
        (path).../apache-solr-4.0.0/example>java -jar start.jar

    2) Start MongoDB
        if you change the permissions of the /data and /data/db folders
            just: mongod
        else
            sudo /mongod

    3) Activate the virtual environments
        (path) source ...\environments\emif\Scripts>activate (for unix users)

    4) Start Django
        python manage.py runserver 0.0.0.0:8000


#### Integrate Sentry

Put in settings.py:

* Sentry url must be specified in settings.py globals, on parameter "SENTRY_URL"

* Also:

```
RAVEN_CONFIG = {
    'dsn': 'http://hash@host:port/id',
}
```


#### Update version

```
python manage.py update_version 0.7
```


#### Developers

 * Luís A. Bastião Silva <bastiao@ua.pt>
 * Ricardo Ribeiro <ribeiro.r@ua.pt> 


#### Lead developer

* Luís A. Bastião Silva <bastiao@ua.pt> (since 2013 until now)

#### Project Leader

 * José Luis Oliveira <jlo@ua.pt>


#### Past Developers

 * Rui Mendes <ruidamendes@ua.pt>
 * José Melo <melojms@gmail.com>
 * Tiago Godinho <tmgodinho@ua.pt>


 Enjoy!
