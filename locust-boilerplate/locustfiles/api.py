from locust import TaskSet, task, between

from common import config
from os import environ
import logging


class APIUserBehavior(TaskSet):
    wait_time = between(5, 10)
    api_token = None
    STATUS = None

    def __init__(self, parent):
        super(APIUserBehavior, self).__init__(parent)
        self.headers = config.HEADERS

    def on_start(self):
        self.user.host = config.BASE_URL
        self.api_token = environ.get("TOKEN")
        if not self.api_token:
            logging.info("Stop test because API was not set. Pls set TOKEN env var")
            self.user.environment.runner.quit()

    @task
    def reload(self):
        token_ = config.API_TOKEN.format(self.api_token)
        if not self.STATUS:
            with self.client.post(''.join((config.get_uri(), config.RELOAD)), name="POST_reload",
                                  headers=dict(Authorization=token_)) as response:
                if config.OK not in response.text:
                    response.failure("Assert failure: {}".format(response.text))
                else:
                    self.STATUS = config.OK

    @task
    def api_test_2(self):
        pass
