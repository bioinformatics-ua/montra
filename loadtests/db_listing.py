from locust import HttpLocust, TaskSet, task
from pyquery import PyQuery

class DBListing(TaskSet):
    def __getCsrf(self):
        r = self.client.get("/")
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


        response = self.client.post("/accounts/signin/", {"identification":"admin", "password":"emif", 'csrfmiddlewaretoken': self.__getCsrf()})

        if response.status_code != 200:
            with open('log.html', 'w+') as file:
                file.write(response.text)

    @task(1)
    def personal(self):
        self.client.get("/databases/")

    @task(1)
    def all(self):
        self.client.get("/alldatabases/")

    @task(1)
    def dashboard(self):
        self.client.get('/dashboard')

    @task(1)
    def dashboard(self):

        self.client.post('/resultsdiff/1', {'query': 'cardiac', 'csrfmiddlewaretoken': self.__getCsrf()})

    @task(1)
    def fingerprint(self):
        self.client.get('/fingerprint/70434bc0e1c797dd4bec194142458e21/1/')



class WebsiteUser(HttpLocust):
    host = "http://127.0.0.1:8000"
    task_set = DBListing
    min_wait=5000
    max_wait=9000
