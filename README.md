<img src="images/box-dev-logo-clip.png" 
alt= “box-dev-logo” 
style="margin-left:-10px;"
width=40%;>
# Admin-Toolkit

## Install
```
pip install -r requirements.txt
```

## Overview

**Do not upload your keys with auth/config.py. Store them elsewhere if possible to prevent accidental upload.**

* Auth
    * `box.py` authenticates your application
    * `config.py` contains the keys to authenticate your application. It also contains items such as folder id's you may want to run your scripts on
* Entrusted Toolkit
    * `boxPrimaryAddresses.py` returns email addresses for a list of usernames.
    * `Collab.py` class stores a folder, its collaborators, and its parent. Used for `collaborations.py`
    * `collaborators.py` recursively searches for new collaborators and outputs them. 
    * `printUserFolders.py` recursively prints the folders under a given folder. Use the syntax in the comments to run
    * `verifyName.py` verifies a prefix from `prefix_list` is included in every folder underneath the given folder.
* Fetch Data and Report
    * `fetch_user_data.py` returns information on every box user in your enterprise. This takes a while to run. Use `user_report.py` on the output to get meaningful data.
    * `user_report.py` shows some meaningful information about the users in your enterprise. Run on the output from `fetch_user_data.py`.
* File Corruption
    * `excel.py` was used to parse information from excel to make a new document.
    * `shared_links.py` creates shared links for every file given an initial folder location. You can choose the type of sharing (everyone, company, folder)