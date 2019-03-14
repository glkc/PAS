from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):

    @task(2)
    def home(self):
        self.client.get("/")

    @task(1)
    def users(self):
        self.client.get("/users")

    @task(3)
    def groups(self):
        self.client.get("/groups")

    @task(4)
    def userById(self):
        self.client.get("/users/104")

    @task(5)
    def groupsByUid(self):
        self.client.get("/users/7/groups")

    @task(6)
    def groupsByGid(self):
        self.client.get("/groups/104")

    @task(7)
    def usersQuery(self):
        self.client.get("/users/query")

    @task(8)
    def groupsQuery(self):
        self.client.get("/groups/query?member={}&member={}".format("landscape", "lp"))


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
