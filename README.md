Montra
=======

[![Join the chat at https://gitter.im/bioinformatics-ua/emif-fb](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/bioinformatics-ua/emif-fb?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This project is being used in the EMIF Platform and it is also know as Fingerprint Browser in the EMIF community.

Some of the Available features:

For Regular user:


* Accounting management (users, databases, workspaces)
* Database management
* Submission and edition (with the former questionary)
* Simple search
* Advanced search
* Results comparison
* Dashboard
* Population Characteristics
* RESTful API


For admin:

* Questions/fingerprints
* Templates
* Templates definition by XLSX

For developers:

* RESTful API
* Plugin based architecture: new modules are possible to include


## Install 

## For Development

#### Note
This guide is provided for Ubuntu 14.04, for other systems or releases instructions may be subject to changes.

All terminal commands can be executed, but whenever we use something between '<', '>' it means that it must be changed for the user. Eg. `<your_path>` --> `/opt/`

#### Install Dependecies in Ubuntu


1.  Install packages

        $   sudo apt-get install git python-pip curl mongodb postgresql rabbitmq-server libxml2-dev libxslt1-dev python-dev libpython-dev build-essential libyaml-dev postgres-server-dev-9.4 libffi cryptography

2. Checkout of the source code

        $   mkdir <your_path>/EMIF-ROOT
        $   cd <your_path>/EMIF-ROOT
        $   git clone -b master https://github.com/bioinformatics-ua/emif-fb.git

    If you're a developer, you can change branch to dev ( see  [DevelopmentCycle](https://github.com/bioinformatics-ua/emif-fb/wiki/DevelopmentCycle "DevelopmentCycle") )

3.  Install virtualenv

        $   sudo pip install virtualenv

4. Activate Virtual Environment

        $   virtualenv <your_path>/EMIF-ROOT/emif
        $   source <your_path>/EMIF-ROOT/emif/bin/activate

5.  Install pil

        $   pip install -r requirements.txt --allow-all-external --allow-unverified pil

6.  Install and Start MongoDB

        $ sudo mkdir <your_mongodb_path>
        $ sudo mkdir <your_mongodb_path>/db

    Now you have 2 hypotheses:

    1.   change the permissions of data and db folders and run "mongod":

            $   sudo chmod a+x <your_mongodb_path>
            $   sudo chmod a+x <your_mongodb_path>/db
            $   mongod --dbpath <your_mongodb_path>

   	2. Run mongod as root:
		
			$	sudo mongod --dbpath <your_mongodb_path>

7. Create '~/.pgpass' file and insert:

        localhost:5432:*:<your_postgres_user>:<your_postgres_pass>

8. Change permission mode of pgpass file

        chmod 600 ~/.pgpass

9.  Install and Configure Apache-solr

    1. Install JDK and JRE:

            $   sudo apt-get update
            $   sudo apt-get install default-jre default-jdk

    2. Download and install SOLR

            $   cd /opt
            $   wget http://archive.apache.org/dist/lucene/solr/4.7.2/solr-4.7.2.tgz
            $   tar -xvf solr-4.7.2.tgz
            $   cp -R solr-4.7.2/example /opt/solr
            $   cd /opt/solr

    3. Go to folder emif-fb-root/conf/solr/ and copy all the files to the solr default core configuration

            $   cp -r <your_path>/EMIF-ROOT/emif-fb/confs/solr/suggestions /opt/solr/confs/
            $   cp -r <your_path>/EMIF-ROOT/emif-fb/confs/solr/collections/* /opt/solr/example/confs/

10. Create a script file:

    1. copy code from:

            https://gist.github.com/bastiao/c8d3be799dc7c257f01a

    2. Paste in a new file in confs/ folder. Eg:

            <your_path>/EMIF-ROOT/emif-fb/confs/script.sh

    3. Open file and change (to the same of the *~/.pgpass* file)

            APP_DB_USER=<your_postgres_user>
            APP_DB_PASS=<your_postgres_pass>

    4. Run the script

            $   sh <your_path>/EMIF-ROOT/emif-fb/confs/<script_name>.sh


11. Run Apache-solr as service

    Go to solr folder and Run:

        $   java -jar /opt/solr/example/start.jar

12. Open a new terminal window/tab and run celery

        $   celery --app=emif.tasks worker -l debug -B

13. Create sp.key and sp.crt files on confs/certificates being them respectively the private key and the public certificate for all comunication originating from third-party IDP's to our SP endpoint

14. The SP endpoint for IDPS uses xmlsec (which is installed through this readme). By default the path to this binary is '/usr/bin/xmlsec1'. If the path on the system is different it should be defined through the variable 'XMLSEC_BIN' on emif/emif/settings.py, otherwise it's okay to leave the default value.

15. Sync Database

        $	python manage.py syncdb
		$	python manage.py import_questionnaire <path_to_fingerprint_schema>
        $	python manage.py migrate
		$	cat <your_path>/EMIF-ROOT/emif-fb/confs/newsletter/newsletter_templates.sql | python manage.py dbshell

16. (Optional/Temporary) Support Developer Group

		$	python manage.py shell
		>>> import utils.developer_group 
		>>> quit()

17. Run Server

        $	python manage.py runserver 0.0.0.0:8000

17. Create a folder to documents population characteristic

        mkdir -p <your_path>/EMIF-ROOT/emif/static/files/

18. Open browser and write

        localhost:8000

### Optional Steps:
1. Create Local Settings File:

        <your_path>/EMIF-ROOT/emif/emif/local_settings.py

2. Add lines for email integration - **Fill accordingly** (optional):

        EMAIL_HOST = 'address.mail.com'
        EMAIL_HOST_PASSWORD = 'passwd'
        EMAIL_HOST_USER = 'login'
        EMAIL_PORT = 25
        EMAIL_USE_TLS = True


3. Add lines for integration with github issues and releases **Fill accordingly** (optional)

        GITHUB_USERNAME='githubusername'
        GITHUB_PASSWD='pass'
        GITHUB_ACCOUNT='bioinformatics-ua'
        GITHUB_REPO='emif-fb'


4. To add a new IDP service to the our SP endpoint just add the service metadata xml file path to IDP_SERVICES array **Fill accordingly** (optional).

        IDP_SERVICES += [path.join(BASEDIR, 'idp_metadata.xml')]


### Start the virtual environment and development (always)
1. Go to solr folder and Run:

        $   java -jar /opt/solr/example/start.jar

2. Start MongoDB

    If you change the permissions of the /data and /data/db folders

        $    mongod --dbpath <your_mongodb_path>

    else

   		$	sudo mongod --dbpath <your_mongodb_path>

3. Activate the virtual environments

   		$	source <your_path>/EMIF-ROOT/emif/bin/activate

4.	Start Django

        $   python manage.py runserver 0.0.0.0:8000

5. Open browser at:

        localhost:8000


----------
##For Production
#### Integrate Sentry

Put in settings.py:

* Sentry url must be specified in settings.py globals, on parameter "SENTRY_URL"

* Also:

```
RAVEN_CONFIG = {
    'dsn': 'http://hash@host:port/id',
}
```

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

#### Project Leader

 * José Luis Oliveira <jlo@ua.pt>



#### Developers

 * Luís A. Bastião Silva <bastiao@ua.pt>
 * Alina Trifan <alina.trifan@ua.pt>
 * André Malta <andremalta@ua.pt>


#### Lead developer

* Luís A. Bastião Silva <bastiao@ua.pt> (since 2013 until now)


#### Past Developers
 * Ricardo Ribeiro <ribeiro.r@ua.pt>
 * Rui Mendes <ruidamendes@ua.pt>
 * José Melo <melojms@gmail.com>
 * Tiago Godinho <tmgodinho@ua.pt>


 Enjoy!
