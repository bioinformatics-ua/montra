emif-fb
=======

EMIF Platform - Fingerprint Browser 


#### Local settings

    $ cat emif/emif/local_settings.py
    EMAIL_HOST = 'address.mail.com'
    EMAIL_HOST_PASSWORD = 'passwd'
    EMAIL_HOST_USER = 'login'
    EMAIL_PORT = 25
    EMAIL_USE_TLS = True


#### Developers

 * Luís A. Bastião Silva <bastiao@ua.pt>
 * Rui Mendes <ruidamendes@ua.pt>
 * Tiago Godinho <tmgodinho@ua.pt>
 * Ricardo Ribeiro <ribeiro.r@ua.pt>
 * José Melo <melojms@gmail.com>

 
#### Project Leader

 * José Luis Oliveira <jlo@ua.pt>


#### Installation steps

1. Checkout of the source code


        https://github.com/bioinformatics-ua/emif-fb.git

2. Create and activate virtual environment


        (path) ...\environments>virtualenv emif
        (path) ...\environments\emif\Scripts>activate.bat (for windows users)
        (path) source ...\environments\emif\Scripts>activate (for unix users)

3. Go to project folder
    
        (emif) C:\...\BioInformatics\emif-fb>   
    
4. Install requirements.txt


        pip install -r requirements.txt

    NOTE: git must be in environment variables and PIP have to be installed.

5. Run


        python manage.py syncdb
        python manage.py migrate
        python manage.py loaddata emif\fixtures\emif_questionary_1.yaml
        python manage.py runserver

6. Run Apache-solr as service


        Go to solr folder and Run
        (path).../apache-solr-4.0.0/example>java -jar start.jar

7. Open browser and write


        localhost:8000


 Enjoy!
