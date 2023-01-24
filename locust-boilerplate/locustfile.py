from locust import FastHttpUser

from locustfiles import mobile, api, web


class TestUser(FastHttpUser):
    tasks = {
        mobile.MobileAppBehavior: 0,
        api.APIUserBehavior: 0,
        web.WebUserBehavior: 100
    }
