import ConfigParser
import csv
import json
import os
import time
from boxsdk.exception import BoxAPIException

import requests

from auth import box

# This is the code from Michigan. It creates a giant xlsx with information for every user in our box enterprise
# It is recommended to run user_report.py on the output to get more detailed information
# I recommend running this in a secure machine on a cron-job. It needs Box creds to run, so I wouldn't recommend AWS

client = box.box_access_token()

if __name__ == "__main__":

    config_path = os.getenv('BUR_CONFIG', os.path.dirname(os.path.realpath(__file__)))
    config = ConfigParser.ConfigParser()
    settings_file = os.path.join(config_path, "settings.conf")
    config.read(settings_file)
    fi = open(os.path.join("output", "user_report.csv"), "wb")
    out = csv.writer(fi, delimiter=',', dialect='excel-tab')

    box_attrs = [f.strip() for f in config.get("user_lookup", "box_attrs").split(",")]

    # change title of column from "box_tracking_codes" to "box_account_type"
    headers = box_attrs[:]
    index = headers.index("tracking_codes")
    headers[index] = "account_type"
    # NOTE we are going to process one line at time so no need for headers
    out.writerow(["username", "retrieved_at"] + ["box_%s" % s for s in headers])

    box_params = {"fields": ",".join(box_attrs)}
    try:
        box_params["limit"] = config.get("user_lookup", "box_request_limit")
    except BoxAPIException:
        box_params["limit"] = 100
    box_params["offset"] = 0
    fetched_count = 0
    while True:

        get_box_users = client.make_request(
            "GET",
            client.get_url('users'),
            params=box_params
        )

        if get_box_users.status_code != requests.codes.ok:
            print("Response code \"%d \"from \"%s\"\n" % (get_box_users.status_code, get_box_users.url))
        body = get_box_users.content
        box_users = json.loads(body)
        if len(box_users["entries"]) < 1:
            break
        fetched_count += len(box_users["entries"])
        print("Fetched %d out of %d." % (fetched_count, box_users["total_count"]))
        for box_user in box_users["entries"]:
            username = box_user["login"].split("@")[0].lower()
            attrs = [username, time.strftime("%Y-%m-%dT%H:%M:%S%z")]
            for key in box_attrs:
                if key == "tracking_codes":
                    if box_user[key]:
                        campus = ""
                        for tracking_code in box_user[key]:
                            if tracking_code["name"] == "Campus":
                                campus = tracking_code["value"].upper()
                        attrs.append(campus)
                    else:
                        attrs.append("individual")
                    continue
                attrs.append(box_user[key])

            # NOTE we need to write one line, then send it to syslog and truncate our virtual file
            out.writerow([unicode(s).encode("ascii", "replace") for s in attrs])

        box_params["offset"] += box_params["limit"]

    fi.close()
