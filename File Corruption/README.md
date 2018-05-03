# File Corruption

## Install
```
pip install -r requirements.txt
```

## Overview

**Do not upload your keys with auth/config.py. Store them elsewhere if possible to prevent accidental upload.**

* Auth
    * `box.py` authenticates your application
    * `config.py` contains the keys to authenticate your application. It also contains items such as folder id's you may want to run your scripts on
* File Corruption
    * `excel.py` was used to parse information from excel to make a new document.
    * `shared_links.py` creates shared links for every file given an initial folder location. You can choose the type of sharing (everyone, company, folder)
    
## Configure
### Excel
Set `xl_file` in `excel.py` with the excel file with corruption information.
### shared_links
Set `base_folder_id` in config and set `access_type` in `shared_links.py` to "everyone", "company", or "folder".

## Examples
### Excel
Input
![ExcelSheet.PNG](img/ExcelSheetFixed.PNG)

Output (each file is one user with their files listed inside)
![output.PNG](img/outputFixed.PNG)