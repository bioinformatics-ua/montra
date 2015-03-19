# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from locust import HttpLocust, TaskSet, task
from pyquery import PyQuery

class DBListing(TaskSet):
    def __getCsrf(self):
        r = self.client.get("/", name="Index")
        pq = PyQuery(r.content)
        csrfs = pq('input[name="csrfmiddlewaretoken"]')
        csrf = [
            l.attrib["value"] for l in csrfs
        ][0]

        return csrf

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        response  = self.client.post("/accounts/signin/", {"identification":"admin", "password":"emif", 'csrfmiddlewaretoken': self.__getCsrf()}, name="Login page")

        #if response.status_code != 200:
        #    with open('log.html', 'w+') as file:
        #        file.write(response.text)

    @task(1)
    def personal(self):
        self.client.get("/databases/", name="Personal Databases")

    @task(1)
    def all(self):
        self.client.get("/alldatabases/", name="All Databases")

    @task(1)
    def datatable(self):
        response = self.client.post('/qs_data_table', {'db_type': 53, 'qsets[]': [491, 492], 'csrfmiddlewaretoken': self.__getCsrf()}, timeout=None,
            name="Datatable")

    @task(1)
    def dashboard(self):
        self.client.get('/dashboard', name='Dashboard')

    @task(1)
    def freetext_search(self):
        self.client.post('/resultsdiff/1', {'query': 'cardiac', 'csrfmiddlewaretoken': self.__getCsrf()}, name='Freetext Search')

    @task(1)
    def advanced_search(self):
        response = self.client.post('/resultsdiff/1', {'qid': 53,
            'boolrelwidget-boolean-representation': '(question_nr_1.01: "ADNI" OR question_nr_1.03: "University")',
            'boolrelwidget-boolean-serialization':'BEGIN_BG_10002BEGIN_VAR_10002BEGIN_BG_10000BEGIN_VAR_10000BEGIN_BG_10005BEGIN_VAR_10005T;;;;;question_nr_1.01;;;;;1.01.%20Cohort%20name;;;;;ADNI;;;;;clearSimple(%22question_1.01%22);OTHER_10005END_VAR_10005BEGIN_REL_10005END_REL_10005END_BG_10005OTHER_10000BEGIN_BG_10003BEGIN_VAR_10003T;;;;;question_nr_1.03;;;;;1.03.%20Institution%20name;;;;;University;;;;;clearSimple(%22question_1.03%22);OTHER_10003END_VAR_10003BEGIN_REL_10003END_REL_10003END_BG_10003OTHER_10000END_VAR_10000BEGIN_REL_10000OR,END_REL_10000END_BG_10000OTHER_10002END_VAR_10002BEGIN_REL_10002END_REL_10002END_BG_10002',
            'question_1.03': 'University',
            'question_1.01': 'ADNI',
            'csrfmiddlewaretoken': self.__getCsrf()}, name='Advanced Search')

    @task(1)
    def fingerprint(self):
        self.client.get('/fingerprint/70434bc0e1c797dd4bec194142458e21/1/', name="Fingerprint Summary")

    @task(1)
    def geolocation(self):
        self.client.get('/geo', name='Geolocation')

    @task(1)
    def privatelinks(self):
        self.client.get('/public/fingerprint', name='Private Links')

    @task(1)
    def apiinfo(self):
        self.client.get('/api-info', name='API Info')

    @task(1)
    def searchhistory(self):
        self.client.get('/advsearch/history', name='Search History')

    @task(1)
    def editdb(self):
        self.client.get('/dbEdit/70434bc0e1c797dd4bec194142458e21/53', name='Edit Database')

    @task(1)
    def adddb(self):
        self.client.get('/advancedSearch/53/1/', name='Add Database')

    @task(1)
    def comparedbs(self):
        self.client.post('/resultscomp', {'chks_cc7f3a8f8af0f6c99f9385c7372c8fe3': 'on',
            'chks_2b9291151f7b3f2fd1fed0d876e59b7a': 'on',
            'chks_2151825ca52388e960d1ed0728dc38b2': 'on',
            'csrfmiddlewaretoken': self.__getCsrf()}, name='Freetext Search')

    @task(1)
    def notifications(self):
        self.client.get('/notifications/', name='Notifications List')

    @task(1)
    def github(self):
        self.client.get('/controlversion/history', name='Project History')

class WebsiteUser(HttpLocust):
    host = "http://127.0.0.1:8000"
    task_set = DBListing
    min_wait=5 * 1000 # stays on page min (ms)
    max_wait=20 * 1000 # stays on page max (ms)
