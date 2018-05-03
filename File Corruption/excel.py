# Import pandas
from __future__ import print_function
import os
import pandas as pd
import csv

# Assign spreadsheet filename to `file`
xl_file = "..\..\Box File Corruption Investigation\EID 81319 - All Affected File Versions (Fixed info as of " \
          "2018-02-27).xlsx "

# Load spreadsheet into two different variables
xl = pd.ExcelFile(xl_file)
xl2 = pd.ExcelFile(xl_file)

# Load Column names
items = xl._parse_excel(sheetname=1).as_matrix(
    ["file_name", "version_created_time", "uploader_email", "file_id", "parent_folder_id"])
count = 0

# Load Column name from sheet 2 to get the list of uploader's on there
unique_users = xl2._parse_excel(sheetname=2, header=0).as_matrix(["uploader_email"])

for user in unique_users:
    current_user = user[0]
    completeName = os.path.join("output", current_user + ".csv")
    myfields = ["file_name", "link_to_file", "parent_folder_id", "version_created_time", "uploader_email"]
    with open(completeName, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=myfields)
        writer.writeheader()
        for item in items:
            if item[2] == current_user:
                try:
                    writer.writerow(
                        {"file_name": str(item[0]),
                         "link_to_file": "=HYPERLINK(\"https://iu.app.box.com/file/" + str(item[3]) + "\")",
                         "parent_folder_id": "=HYPERLINK(\"https://iu.app.box.com/folder/" + str(item[4]) + "\")",
                         "version_created_time": str(item[1]),
                         "uploader_email": str(item[2])
                         }
                    )

                except:
                    count += 1
                    print("Non alphanumeric characters for: " + str(item[2]))
                    writer.writerow({"file_name": "*non characters*",  ### ADDRESS THIS ###
                                     "link_to_file": "=HYPERLINK(\"https://iu.app.box.com/file/" + str(item[3]) + "\")",
                                     "parent_folder_id": "=HYPERLINK(\"https://iu.app.box.com/folder/" + str(
                                         item[4]) + "\")",
                                     "version_created_time": str(item[1]),
                                     "uploader_email": str(item[2])})

print(str(count) + " Exceptions")
