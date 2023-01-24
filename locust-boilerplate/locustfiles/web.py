import gevent
import re
import logging

from locust import between, task, SequentialTaskSet, events
from locust_plugins.transaction_manager import TransactionManager
from locust.runners import STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP, WorkerRunner
from locust_plugins import listeners
from time import time, sleep
from common import config


class WebUserBehavior(SequentialTaskSet):
    tm = None
    x_var_username = ''
    x_var_email = ''
    x_var_password = ''
    auth = ''
    wait_time = between(5, 10)

    def on_start(self):
        self.tm = TransactionManager()
        self.x_var_password = config.TEMP_PWD

    @task
    def happy_path_scn(self):
        self.open_swagger()
        self.get_todos()
        self.open_register()
        self.submit_register()
        self.open_login()
        self.login()
        self.open_home()
        self.open_profile()

    def open_swagger(self):
        self.tm.start_transaction("01_Open_Swagger")
        with self.client.get("/", name="GET_main", catch_response="True") as response:
            home_page_assertion = 'Test API'
            if home_page_assertion not in response.text:
                response.failure("Assert failure: {} not exists".format(home_page_assertion))
        self.tm.end_transaction("01_Open_Swagger")

    def get_todos(self):
        self.tm.start_transaction("02_Open_Todos")
        with self.client.get("/todos/", name="GET_todos", catch_response="True") as response:
            home_page_assertion = 'Test API'
            resp = re.search('''"id": (.+?),''', response.text, re.IGNORECASE).group(1)
            if not resp:
                response.failure("Assert failure: {} not exists".format(home_page_assertion))
        self.tm.end_transaction("02_Open_Todos")

    def open_register(self):
        self.tm.start_transaction("03_Open_register")
        with self.client.get("/login/register", name="GET_register", catch_response="True") as response:
            reg_assertion = 'Register'
            if reg_assertion not in response.text:
                msg = "Assert failure: '{}' not exists".format(reg_assertion)
                response.failure(msg)
        self.tm.end_transaction("03_Open_register")

    def submit_register(self):
        tm_name = "04_Submit_register"
        id_ = str(time()).replace('.', '')
        self.x_var_username = f'temps{id_}'
        logging.debug(f"username: {self.x_var_username}")
        self.x_var_email = f"{self.x_var_username}@test.com"
        self.tm.start_transaction(tm_name)
        post_data = dict(username=self.x_var_username, password=self.x_var_password,
                         email=self.x_var_email)
        with self.client.post("/login/register", name="POST_register", data=post_data,
                              catch_response="True") as response:
            reg_assertion = 'Thanks for registering!'
            if reg_assertion not in response.text:
                msg = "Assert failure: '{}' not exists".format(reg_assertion)
                response.failure(msg)
        self.tm.end_transaction(tm_name)

    def open_login(self):
        tm_name = '05_Open_login'
        self.tm.start_transaction(tm_name)
        with self.client.get("/login/", name="GET_login", catch_response="True") as response:
            reg_assertion = 'Login'
            if reg_assertion not in response.text:
                msg = "Assert failure: {} not exists".format(reg_assertion)
                print(response.text)
                response.failure(msg)
        self.tm.end_transaction(tm_name)

    def login(self):
        tm_name = '06_Submit_login'
        self.tm.start_transaction(tm_name)
        post_data = dict(username=self.x_var_username, password=self.x_var_password)
        with self.client.post("/login/", name="POST_login", data=post_data, catch_response="True") as response:
            if 'Set-Cookie' in response.headers:
                self.auth = response.headers['Set-Cookie'].replace('session=e', '')
            else:
                response.failure("Assert failure: AUTH headers not exists")
        self.tm.end_transaction(tm_name)

    def open_home(self):
        tm_name = '07_Click_open_home'
        self.tm.start_transaction(tm_name)
        with self.client.get("/home", name="GET_open_home", catch_response="True") as response:
            assertion_mg = 'Rodman'
            if assertion_mg not in response.text:
                response.failure("Assert failure: '{}' not exists".format(assertion_mg))
        self.tm.end_transaction(tm_name)

    def open_profile(self):
        tm_name = '08_Open_validate_profile_info'
        self.tm.start_transaction(tm_name)
        with self.client.get("/home/profile", name="GET_profile", catch_response="True") as response:
            if self.x_var_email not in response.text:
                response.failure("Assert failure: '{}' not exists".format(self.x_var_email))
        self.tm.end_transaction(tm_name)


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    # make sure this is the last request event handler you register, as later ones will not get triggered
    # if there is a failure
    listeners.RescheduleTaskOnFail(environment)


@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 5.0:
        logging.error("Test failed due to failure ratio > 5%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 1000:
        logging.error("Test failed due to average response time ratio > 1000 ms")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 800:
        logging.error("Test failed due to 95th percentile response time > 800 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0


def checker(environment):
    while environment.runner.state not in [STATE_STOPPING, STATE_STOPPED, STATE_CLEANUP]:
        sleep(1)
        if environment.runner.stats.total.fail_ratio > 0.5:
            logging.info(f"fail ratio was {environment.runner.stats.total.fail_ratio}, quitting")
            environment.process_exit_code = 2
            environment.runner.quit()
            return


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    if not isinstance(environment.runner, WorkerRunner):
        gevent.spawn(checker, environment)
