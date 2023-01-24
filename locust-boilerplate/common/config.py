###
# API
###
BASE_URL = "https://www.pythonanywhere.com"
BASE_PATH = "/api"
API_VERSION = "/v0"
API_TOKEN = "Token {}"
ACCESS_TOKEN = ""
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json"
}
OK = "OK"
RELOAD = "/user/Karens/webapps/Karens.pythonanywhere.com/reload/"

###
# SCN Constants
###
NF = "NOT_FOUND"
TEMP_PWD = "temps"
email = "NOT_FOUND"
password = "NOT_FOUND"


def get_uri():
    return f"{BASE_URL}{BASE_PATH}{API_VERSION}"
