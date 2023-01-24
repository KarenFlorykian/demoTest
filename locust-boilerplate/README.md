### Getting started 
Read the docs [here](https://docs.locust.io/en/stable/quickstart.html)

## Where to put test files for upload?
Entrypoint is `locustfile.py` with list of scenarios and probabilities.
Test scripts located in `locustfiles` folder.

## How to run the tests?
```sh
$ python3 -m venv ./venv 
$ source venv/bin/activate
$ pip install -r requirements.txt
$ locust -f locustfile.py -H=https://karens.pythonanywhere.com -u 1 -r 1 --headless --run-time=30s --print-stats --csv=first_report --logfile=first_report.log --log-transactions-in-file --html=first_report.html --csv-full-history --check-fail-ratio
```
Then open `first_report.html` file with test results.  
