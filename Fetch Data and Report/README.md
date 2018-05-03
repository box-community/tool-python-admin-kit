# Fetch Data and Report

## Install
```
pip install -r requirements.txt
```

## Overview

**Do not upload your keys with auth/config.py. Store them elsewhere if possible to prevent accidental upload.**

* Auth
    * `box.py` authenticates your application
    * `config.py` contains the keys to authenticate your application. It also contains items such as folder id's you may want to run your scripts on
* Fetch Data and Report
    * `fetch_user_data.py` returns information on every box user in your enterprise. This takes a while to run. Use `user_report.py` on the output to get meaningful data.
    * `user_report.py` shows some meaningful information about the users in your enterprise. Run on the output from `fetch_user_data.py`.
    
Example Output from `fetch_user_data.py`
![excel.PNG](img/excel.PNG)

Example Output from `user_report.py`
![user_report.PNG](img/user_reportEdited.PNG)